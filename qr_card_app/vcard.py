import vobject

def generate_vcard(first_name, last_name, email, phone):
    vcard = vobject.vCard()
    vcard.add('n')
    vcard.n.value = vobject.vcard.Name(family=last_name, given=first_name)
    vcard.add('fn')
    vcard.fn.value = f"{first_name} {last_name}"
    vcard.add('email')
    vcard.email.value = email
    vcard.email.type_param = 'INTERNET'
    vcard.add('tel')
    vcard.tel.value = phone
    vcard.tel.type_param = 'CELL'
    return vcard.serialize()