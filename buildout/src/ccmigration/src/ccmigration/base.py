# -*- coding: utf-8 -*-
import erppeek
import smtplib
from email.mime.text import MIMEText
from traceback import print_exc


default_options = (
    (
        "--source",
        "-s",
        {
            'type': str,
            'default': "source",
            'action': 'store',
            'help': (
                u"Odoo source environment name "
                u"- specified in erppeek.ini file")
        }
    ),
    (
        "--destination",
        "-d",
        {
            'type': str,
            'default': "destination",
            'action': 'store',
            'help': (
                u"Odoo destination environment name "
                u"- specified in erppeek.ini file")
        }

    ),
    (
        "--configuration",
        "-c",
        {
            'default': 'erppeek.ini',
            'action': 'store',
            'help': 'erppeek.ini path'
        }
    ),
    (
        "--limit",
        "-l",
        {
            'type': int,
            'help': 'Limit number of record to import'
        }
    ),
    (
        "--offset",
        "-o",
        {
            'type': int,
            'default': 0,
            'help': 'Limit number of record to import'
        }
    ),
    (
        "--update",
        "-u",
        {
            'action': 'store_true',
            'help': 'Update existent record. False by default (that is: do not update)'
        }
    ),
    (
        "--noskip",
        "-n",
        {
            'action': 'store_true',
            'help': 'Skip existent record. True by default (that is: skip them)'
        }
    ),
    (
        "--debug",
        "-D",
        {
            'action': 'store_true',
            'help': 'Activate debug mode. More permissive on a few migrations.'
        }
    ),
    (
        "--dry",
        "-r",
        {
            'action': 'store_true',
            'help': 'Activate dry-run mode. No writes or creates.'
        }
    ),
    (
        "--notify",
        "-N",
        {
            'action': 'store_true',
            'help': 'If set, the migration will send emails.'
        }
    )
)

ME = 'info@example.com'
TO = 'germano.guerrini@gmail.com'


class MockNew(object):
    def __init__(self):
        self.id = 0
        self.name = 'mock'


class BaseCommand(object):
    """Base migration command you must inherit from this class
    to create a new command.

    To create a new command you have to define the *_fields* attribute
    and implement the *migration* method.

    See: partner.PartnerMigration for an example
    """

    # default options from config
    options = default_options

    # default context for openerp
    default_context = {'lang': 'it_IT'}

    # Se un related field restituisce più valori di default solleva un eccezione.
    # Se invece il flag è True prende il primo.
    # Se è un intero, prende quello con l'indice specificato (MOOOOLTA cautela).
    # Utilizzato solo da saleorder per cantiericasa in quanto esiste lo stesso
    # partner come fornitore e come cliente.
    # Idealmente si dovrebbe essere in grado di distinguerlo passando una lista
    # di campi e non solo 'name'
    _ignore_to_many_values = False

    _fields = {}

    _default_values = {}

    def __init__(self, config):
        """This method instanciates:
        * config attribute that contains command line arguments
        * source attribute: an instance of erppeek.Client
                            to define the Odoo source environment
        * destination attribute: an instance of erppeek.Client
                                 to define the Odoo destination environment

        """
        self.config = config
        # XXX: override default config file position form command line arg
        erppeek.Client._config_file = config['configuration']

        self.source = erppeek.Client.from_config(config['source'])
        self.source.context = self.default_context

        self.destination = erppeek.Client.from_config(config['destination'])
        self.destination.context = self.default_context

        self.skip_duplicated = not self.config['noskip']
        self.update_existent = self.config['update']
        self.dry_run = self.config['dry']
        print self.skip_duplicated
        print self.update_existent
        print self.dry_run

    def _get_model(self, env, dotted_name):
        """It transforms an openerp model name to erppeek method
        and returns it"""
        return getattr(
            env,
            erppeek.mixedcase(dotted_name)
        )

    def _get_relation_id_by_field(self, env, model_dotted_name,
                                  value, field='name', create=False,
                                  operator='=', transform=None):
        """It search for a record by 'field' and return its id, if it found it
        """
        model = self._get_model(env, model_dotted_name)
        if transform is not None:
            value = transform(value)
        ids = model.search([(field, operator, value)],
            context=self.default_context)
        n_ids = len(ids)
        if n_ids == 1:
            return ids[0]
        elif n_ids == 0:
            if create:
                if not self.dry_run:
                    return model.create({field: value}).id
                else:
                    return 0
            else:
                msg = u"Value not found for {} - {}".format(model._name, value)
                if self.config['debug']:
                    print msg
                else:
                    raise KeyError(msg)
        if not self.config['debug']:
            if self._ignore_to_many_values == False:
                raise KeyError(
                    u"Too many value for {} - {}".format(model._name, value)
                )
            if self._ignore_to_many_values == True:
                return ids[0]
            else:
                return ids[self._ignore_to_many_values]

    def _set_value_for_line(self, old, new, field, model, new_field=None,
                            lookup=None, default=None, force=False):
        """Used in custom setters to migrate the value of a m2m or o2m field.
        It looks in the model for an instance that has the same name of the old
        relation.
        If not found and debug is False, it raises a KeyError.

        TODO: it needs some love to handle a wider spectrum of cases.
        """
        new_field = new_field or field
        value = getattr(old, field)
        if value:
            if lookup is None:
                domain = [('name', '=', value.name)]
            else:
                domain = lookup(value)
            id_ = getattr(self.destination, model).search(
                domain,
                context=self.default_context
            )
            if len(id_) != 1:
                if default is None:
                    err = u"{} {} not found or multiple {}s found ({})".format(
                        model, value.name, model, len(id_))
                    if self.config['debug']:
                        print err
                    else:
                        raise KeyError(err)
                else:
                    new[new_field] = default
            else:
                new[new_field] = id_[0]
        else:
            if force and default is not None:
                new[new_field] = default

    def build_record(self, el, fast=False, force_fast_fields=['name']):
        """Build a record from ``el`` and transform all fields data
        necessary for the migration from _fields attribute.
        If ``fast`` is True, then skip all complicated fields (used to check
        whether an object is a duplicate).

        If the record cannot be safely build for whatever reason, a subclass can
        override the method and return None. This will cause the migration to
        skip said record.

        Note: subclasses must call super implementation if they want to
        override this method.

        TODO: Ideally we should specify in the _fields attribute what fields
              are to be used as a key
        """
        record = self._default_values.copy()

        for f_name, f_desc in self._fields.items():
            value = getattr(el, f_name)
            if not f_desc:
                # Simple field with the same name and same type
                record[f_name] = value
            else:
                if not fast or f_name in force_fast_fields:
                    f_type = f_desc.get('type', None)
                    f_transform = f_desc.get('transform', None)
                    # TODO: implements o2m fields type if possible
                    if f_type in ('m2o', 'many2one'):
                        # skip empty values unless we are updating
                        if not value:
                            if self.update_existent:
                                record[f_desc['name']] = value
                            continue
                        _field = f_desc.get('unique_field', 'name')
                        _unique_value = getattr(value, _field)
                        value = self._get_relation_id_by_field(
                            self.destination,
                            f_desc['relation'],
                            _unique_value,
                            _field,
                            f_desc.get('create', False),
                            transform=f_transform
                        )
                        if value is not None:
                            record[f_desc['name']] = value
                    elif f_type in ('m2m', 'many2many'):
                        original_ids = value
                        value = []

                        # skip empty values unless we are updating
                        if len(original_ids) == 0 and not self.update_existent:
                            continue

                        for v in original_ids:
                            _field = f_desc.get('unique_field', 'name')
                            _unique_value = getattr(v, _field)

                            value.append(self._get_relation_id_by_field(
                                self.destination,
                                f_desc['relation'],
                                _unique_value,
                                _field,
                                f_desc.get('create', False),
                                transform=f_transform
                            ))
                        record[f_desc['name']] = value
                    elif f_type == "custom":
                        setter = getattr(self, f_desc['setter'])
                        setter(el, record)
        return record

    def get_migration_data(self):
        """Prepare migration data by define four attributes:
        * source_model: erppeek instance of Odoo model used as source
        * dest_model: erppeek instance of Odoo model used as destination
        * source_model_ids: source ids used for get migration data
        * source_data: data used for the migration process

        See. partner.PartnerMigration for an example implementation
        """
        raise NotImplementedError

    def check_existent(self, record):
        """Search for duplicated records.
        """
        return self.dest_model.search(
            [('name', '=', record['name'])],
            context=self.default_context
        )

    def set_related_partner_id(self, old, new, field):
        """Set a field related to a partner in those case when in openerp 6
        we got an address reference.
        """
        old_partner = getattr(old, field, False)
        if not old_partner:
            return

        partner_id = old_partner.partner_id
        partner = self.destination.ResPartner.search(
            [
                '&',
                ('name', '=', partner_id.name),
                ('vat', '=', partner_id.vat)
            ],
            context=self.default_context)

        if len(partner) != 1:
            if self.config['debug']:
                print "Error"
            else:
                raise KeyError("Multiple partners or partner not found")
        else:
            new[field] = partner[0]

    def set_user_id(self, old, new, field_name='user_id', force_admin=True):
        user = getattr(old, field_name)
        if not user:
            return
        value = self.destination.ResUsers.search([
            ('name', '=', user.name),
            '|',
            ('active=False'),
            ('active=True')
        ])
        if len(value) == 1:
            new[field_name] = value[0]
        else:
            if force_admin:
                print "Forcing administrator, missing {}".format(user.name)
                new[field_name] = 1

    def migrate(self):
        self.get_migration_data()

        n_created = 0
        n_updated = 0
        n_skipped = 0
        n_invalid = 0
        n_total = len(self.source_data)
        print "{} records founds to migrate".format(n_total)
        for index, data in enumerate(self.source_data, 1):
            # We build an incomplete record as fast as possible just to check
            # for duplicates
            record = self.build_record(data, fast=True)
            if record is None:
                # Bail out
                n_invalid += 1
                print u"[{}/{}] Invalid {}".format(
                    index,
                    n_total,
                    self.dest_model._name
                )
                continue
            check_id = self.check_existent(record)
            if check_id and self.skip_duplicated:
                n_skipped += 1
                print u"[{}/{}] Skip {} - {}".format(
                    index,
                    n_total,
                    self.dest_model._name,
                    record.get('name')
                )
                continue
            # It's not a duplicate: build the entire object
            record = self.build_record(data)
            if record is None:
                # Bail out
                n_invalid += 1
                print u"[{}/{}] Invalid {}".format(
                    index,
                    n_total,
                    self.dest_model._name
                )
                continue
            try:
                if check_id and self.update_existent and not self.skip_duplicated:
                    # EXPERIMENTAL: If a RecordList has been emptied, simply
                    # passing an empty list to 'write' doesn't work as
                    # expected, that is:
                    #
                    #     Model.write(id, {'some_list_field': []})
                    #
                    # will not really set the field to an empty list.
                    # The only way to achieve that is to unlink the field.
                    # So we assume that if a field in the record has an empty
                    # list as its value, we should invoke unlink on it.
                    for field, value in record.iteritems():
                        if value == []:
                            getattr(self.dest_model.browse(check_id)[0], field).unlink()

                    if not self.dry_run:
                        self.dest_model.write(check_id, record)
                    n_updated += 1
                    print u"[{}/{}] Update {} - {} - {}".format(
                        index,
                        n_total,
                        self.dest_model._name,
                        record.get('name'),
                        check_id
                    )
                    continue
            except Exception, e:
                print "Cannot check existent"
                self.send_exception_mail("Cannot check existent")
                import pdb; pdb.set_trace()

            try:
                if not self.dry_run:
                    new = self.dest_model.create(record, context=self.default_context)
                else:
                    new = MockNew()
            except Exception, e:
                print "Cannot create"
                self.send_exception_mail("Cannot create")
                print e
                import pdb; pdb.set_trace( )
            n_created += 1
            print u"[{}/{}] Create {} - {} - {}".format(
                index, n_total, self.dest_model._name, new.name, new.id
            )

        print u"Created {} records".format(n_created)
        print u"Updated {} records".format(n_updated)
        print u"Skipped {} records".format(n_skipped)
        print u"Invalid {} records".format(n_invalid)

    def _send_mail(self, subject, content):
        if not self.config['notify']:
            return
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = ME
        msg['To'] = TO
        try:
            print "sending email"
            s = smtplib.SMTP('localhost')
            s.sendmail(ME, [TO], msg.as_string())
            s.quit()
        except Exception:
            # Diaper
            print "sorry, I can't"
            pass

    def send_exception_mail(self, content):
        subject = 'Exception during {} migration'.format(self.dest_model._name)
        content = content
        self._send_mail(content, subject)

    def send_finish_mail(self):
        subject = '{} migration completed'.format(self.dest_model._name)
        content = 'Done'
        self._send_mail(content, subject)

    @classmethod
    def main(cls, args_):
        """Instanciate a class with command line arguments
        """
        migrator = cls(vars(args_))
        try:
            migrator.migrate()
            migrator.send_finish_mail()
        except:  # pylint: disable=W0702
            migrator.send_exception_mail('Other error')
            print_exc()
            return -1
        return 0
