# -*- coding: utf-8 -*-
from .base import BaseCommand
from .address import AddressMixin

ids = [
    583, 12, 557, 42, 43, 609, 561, 53, 603, 472, 66, 390, 76, 458, 85, 544,
    100, 104, 106, 446, 123, 134, 477, 143, 152, 566, 515, 168, 473, 182, 198,
    200, 388, 230, 235, 239, 241, 455, 263, 267, 279, 517, 528, 299, 309, 311,
    559, 598, 318, 596, 334, 563, 511
]


class FixContacts(BaseCommand, AddressMixin):

    def get_parent_id(self, contact):
        old_parent = contact.partner_id
        if not old_parent:
            return

        parent = self.destination.ResPartner.search(
            [
                '&',
                ('name', '=', old_parent.name),
                ('vat', '=', old_parent.vat)
            ],
            context=self.default_context)

        if len(parent) != 1:
            print "Error '%s' [{} found]" % (old_parent.name, len(parent))
        else:
            return parent[0]

    def prepare(self, contact):
        values = self.get_address_value(contact)
        for field in ('active', 'name', 'type'):
            values[field] = getattr(contact, field)
        values['company_id'] = 1
        return values

    def migrate(self):

        # Slow way
        #partners = self.source.ResPartner.browse([])
        #partners = [
        #    p for p in partners
        #    if len(p.address) > 1 and p.address[-1].name == p.name
        #]

        # Fast way
        partners = self.source.ResPartner.browse([('id', 'in', ids)])
        total = len(partners)
        print "%s partners found" % total

        for index, partner in enumerate(partners, 1):
            # La situazione è la seguente:
            # - il primo contatto del partner è stato utilizzato
            #   per l'anagrafica, invece è un contatto a se stante
            # - l'ultimo contatto del partner contiente l'anagrafica vera ed
            #   invece non è stato importato
            #
            # Pertanto:
            # - genero un nuovo partner a partire dal primo contatto
            # - aggiorno l'anagrafica del partner con l'ultimo
            contact = partner.address[0]
            parent_id = self.get_parent_id(contact)
            if parent_id is not None:
                contact_values = self.prepare(contact)
                contact_values['parent_id'] = parent_id
                exists = len(self.destination.ResPartner.browse([
                    ('name', '=', contact.name)
                ], context=self.default_context)) > 0
                if not exists:
                    self.destination.ResPartner.create(contact_values,
                        context=self.default_context)
                    print "[%s/%s] created %s" % (index, total, contact.name)
                else:
                    print "[%s/%s] skipped %s" % (index, total, contact.name)

            contact = partner.address[-1]
            parent_id = self.get_parent_id(contact)
            if parent_id is not None:
                contact_values = self.prepare(contact)
                self.destination.ResPartner.write(parent_id,
                    contact_values)

        # Aggiorno il flag is_company:
        # tutti quelli che erano res.partner sul vecchio sistema, devono avere is_company = True

        # Reset
        self.destination.ResPartner.browse([]).write({'is_company': False})
        # Set
        self.destination.ResPartner.browse(
            ['parent_id=False']
        ).write({'is_company': True})
