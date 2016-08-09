# -*- coding: utf-8 -*-


class AddressMixin(object):
    """Address mixin used for partner and contact
    """

    def get_address_value(self, address):
        """Retrieve partner address data from res.partner.address model
        """
        values = {}

        simple_fields = [
            "city",
            "email",
            "fax",
            "mobile",
            "phone",
            "street",
            "street2",
            "zip"
        ]
        for f_name in simple_fields:
            value = getattr(address, f_name)
            values[f_name] = value

        related_fields = (
            ("country_id", 'res.country'),
        )

        for f_name, model_name in related_fields:
            value = getattr(address, f_name)
            if not value:
                continue
            value = self._get_relation_id_by_field(
                self.destination, model_name, value.name, 'name', create=False
            )
            values[f_name] = value

        # address.province translates to state_id
        # the region is lost
        if address.province:
            value = self._get_relation_id_by_field(
                self.destination, 'res.country.state',
                address.province.name, 'name', create=False,
                operator='=ilike'
            )
            values['state_id'] = value

        return values
