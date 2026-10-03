from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re


ROOT = Path(__file__).resolve().parent
EXTERNAL_SCHEMES = {'data', 'http', 'https', 'javascript', 'mailto', 'tel'}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.references = []
        self.forms = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get('id'):
            self.ids.add(attributes['id'])
        if tag == 'form':
            self.forms.append(attributes)
        for name in ('href', 'src', 'poster'):
            if attributes.get(name):
                self.references.append(attributes[name])
        for value in re.findall(r'url\(["\']?([^"\')]+)', attributes.get('style', ''), re.I):
            self.references.append(value)

    def handle_data(self, data):
        self.text.append(data)


errors = []
pages = {}
for path in sorted(ROOT.glob('*.html')):
    parser = PageParser()
    parser.feed(path.read_text(encoding='utf-8'))
    pages[path.resolve()] = parser

for path, parser in pages.items():
    for reference in parser.references:
        target = urlsplit(reference.strip())
        if target.scheme.lower() in EXTERNAL_SCHEMES or target.netloc:
            continue
        destination = (path.parent / unquote(target.path)).resolve() if target.path else path
        if target.path and not destination.is_file():
            errors.append(f'{path.name}: missing local target {reference}')
            continue
        if target.fragment:
            target_page = pages.get(destination)
            if target_page and unquote(target.fragment) not in target_page.ids:
                errors.append(f'{path.name}: missing #{unquote(target.fragment)} on {destination.name}')

contact = pages.get((ROOT / 'contact.html').resolve())
if not contact:
    errors.append('contact.html is missing')
else:
    mail_forms = [form for form in contact.forms if 'data-rpai-mail-form' in form]
    if len(mail_forms) != 2:
        errors.append('contact.html must retain the prayer-request and connect-card forms')
    for anchor in ('prayer-request', 'connect-card'):
        if anchor not in contact.ids:
            errors.append(f'contact.html is missing the #{anchor} link target')
    subjects = {form.get('data-subject') for form in mail_forms}
    if subjects != {'Prayer request for RPAI', 'New connection with RPAI'}:
        errors.append('contact.html form subjects do not match the known-good forms')

ministry = pages.get((ROOT / 'ministry.html').resolve())
if not ministry:
    errors.append('ministry.html is missing')
else:
    ministry_text = ' '.join(ministry.text)
    for marker in ('Royal Men', 'Virtuous', 'NextGen', 'Home Cell', 'Branch Fellowships'):
        if marker not in ministry_text:
            errors.append(f'ministry.html is missing expected ministry content: {marker}')

if errors:
    print('SITE CHECK FAILED:')
    for error in errors:
        print(f'- {error}')
    raise SystemExit(1)

print(f'SITE CHECK PASSED: {len(pages)} pages and all local links/anchors resolve.')
print('Contact forms and expected ministry sections are present.')
