/*
 * RPAI language switcher.
 *
 * World languages (English, Hindi, French, German, Italian, Portuguese,
 * Russian, Spanish) are translated across the entire page by Google's
 * translation service, called directly in small batches. No widget,
 * banner or floating icon is ever shown; the site's own dropdown is the
 * only visible control. This covers every heading, paragraph, button,
 * link and menu item on every page.
 *
 * Zambian languages (Bemba, Nyanja, Tonga, Lozi, Tumbuka) use the built-in
 * dictionary below, because Google does not offer them yet. The dictionary
 * also supplies the interface labels while the full-page engine starts.
 *
 * Church names ("Dunamis"), bank names, account names, account numbers and
 * the PayPal brand are marked notranslate so they never change.
 */
(function () {
	'use strict';

	var STORAGE_KEY = 'rpai.lang';

	var LANGUAGES = [
		{ code: 'bem', name: 'Bemba', htmlLang: 'bem', google: 'bem', group: 'zambian' },
		{ code: 'nya', name: 'Nyanja', htmlLang: 'ny', google: 'ny', group: 'zambian' },
		{ code: 'toi', name: 'Tonga', htmlLang: 'toi', google: null, group: 'zambian' },
		{ code: 'loz', name: 'Lozi', htmlLang: 'loz', google: null, group: 'zambian' },
		{ code: 'tum', name: 'Tumbuka', htmlLang: 'tum', google: 'tum', group: 'zambian' },
		{ code: 'en', name: 'English', htmlLang: 'en', google: 'en', group: 'world' },
		{ code: 'hi', name: 'Hindi', htmlLang: 'hi', google: 'hi', group: 'world' },
		{ code: 'fr', name: 'French', htmlLang: 'fr', google: 'fr', group: 'world' },
		{ code: 'de', name: 'German', htmlLang: 'de', google: 'de', group: 'world' },
		{ code: 'it', name: 'Italian', htmlLang: 'it', google: 'it', group: 'world' },
		{ code: 'pt', name: 'Portuguese', htmlLang: 'pt', google: 'pt', group: 'world' },
		{ code: 'ru', name: 'Russian', htmlLang: 'ru', google: 'ru', group: 'world' },
		{ code: 'es', name: 'Spanish', htmlLang: 'es', google: 'es', group: 'world' }
	];

	var NAV_KEYS = {
		'index.html': 'nav.home',
		'about.html': 'nav.about',
		'ministry.html': 'nav.ministries',
		'gallery.html': 'nav.gallery',
		'daily-devotional.html': 'nav.devotional',
		'announcements.html': 'nav.announcements',
		'branches-transport.html': 'nav.branches',
		'give.html': 'nav.give',
		'contact.html': 'nav.contact'
	};

var DICTIONARY = {
		en: {
			'nav.home': 'Home',
			'nav.about': 'About',
			'nav.ministries': 'Ministries',
			'nav.gallery': 'Gallery',
			'nav.devotional': 'Daily Devotional',
			'nav.announcements': 'Announcements',
			'nav.branches': 'Branches & Transport',
			'nav.give': 'Give',
			'nav.contact': 'Contact',
			'lang.zambian': 'Zambian languages',
			'lang.world': 'World languages',
			'lang.select': 'Select language',
			'give.subheading': 'Partner with us',
			'give.title': 'Give',
			'give.heroLead': 'Your giving supports local outreach, building expansion, and the spread of the Gospel across Zambia.',
			'give.ways': 'Ways to give',
			'give.details': 'Giving details',
			'give.banks': 'Zambian banks',
			'give.banksLead': 'Give directly to any of our Zambian bank accounts. Please use your name as the reference so the church can acknowledge your gift.',
			'give.paypal': 'International giving',
			'give.paypalLead': 'Giving from outside Zambia? Use our only international gateway, PayPal.',
			'give.paypalButton': 'Give via PayPal',
			'give.help': 'For help with any of these details, contact the church office.',
			'give.email': 'Email the church',
			'give.call': 'Call',
			'label.accountName': 'Account name',
			'label.accountNumber': 'Account number',
			'label.centre': 'Centre',
			'footer.follow': 'Follow us'
		},
		fr: {
			'nav.home': 'Accueil',
			'nav.about': 'À propos',
			'nav.ministries': 'Ministères',
			'nav.gallery': 'Galerie',
			'nav.devotional': 'Dévotion quotidienne',
			'nav.announcements': 'Annonces',
			'nav.branches': 'Antennes et transport',
			'nav.give': 'Donner',
			'nav.contact': 'Contact',
			'lang.zambian': 'Langues zambiennes',
			'lang.world': 'Langues du monde',
			'lang.select': 'Choisir la langue',
			'give.subheading': 'Soyez notre partenaire',
			'give.title': 'Donner',
			'give.heroLead': 'Vos dons soutiennent l’action locale, l’agrandissement du bâtiment et la diffusion de l’Évangile en Zambie.',
			'give.ways': 'Façons de donner',
			'give.details': 'Détails pour donner',
			'give.banks': 'Banques zambiennes',
			'give.banksLead': 'Donnez directement sur l’un de nos comptes bancaires zambiens. Indiquez votre nom comme référence afin que l’église puisse reconnaître votre don.',
			'give.paypal': 'Dons internationaux',
			'give.paypalLead': 'Vous donnez depuis l’étranger ? Utilisez notre unique passerelle internationale, PayPal.',
			'give.paypalButton': 'Donner via PayPal',
			'give.help': 'Pour toute aide concernant ces informations, contactez le bureau de l’église.',
			'give.email': 'Écrire à l’église',
			'give.call': 'Appeler',
			'label.accountName': 'Nom du compte',
			'label.accountNumber': 'Numéro de compte',
			'label.centre': 'Centre',
			'footer.follow': 'Suivez-nous'
		},
		de: {
			'nav.home': 'Startseite',
			'nav.about': 'Über uns',
			'nav.ministries': 'Dienste',
			'nav.gallery': 'Galerie',
			'nav.devotional': 'Tägliche Andacht',
			'nav.announcements': 'Ankündigungen',
			'nav.branches': 'Gemeinden und Transport',
			'nav.give': 'Spenden',
			'nav.contact': 'Kontakt',
			'lang.zambian': 'Sambische Sprachen',
			'lang.world': 'Weltsprachen',
			'lang.select': 'Sprache wählen',
			'give.subheading': 'Werden Sie unser Partner',
			'give.title': 'Spenden',
			'give.heroLead': 'Ihre Spende unterstützt die lokale Arbeit, den Ausbau des Gebäudes und die Verbreitung des Evangeliums in ganz Sambia.',
			'give.ways': 'Möglichkeiten zu spenden',
			'give.details': 'Spendeninformationen',
			'give.banks': 'Sambische Banken',
			'give.banksLead': 'Spenden Sie direkt auf eines unserer sambischen Bankkonten. Bitte geben Sie Ihren Namen als Verwendungszweck an, damit die Kirche Ihre Spende zuordnen kann.',
			'give.paypal': 'Internationale Spenden',
			'give.paypalLead': 'Sie spenden außerhalb Sambias? Nutzen Sie unser einziges internationales Zahlungsportal, PayPal.',
			'give.paypalButton': 'Über PayPal spenden',
			'give.help': 'Bei Fragen zu diesen Angaben wenden Sie sich bitte an das Kirchenbüro.',
			'give.email': 'E-Mail an die Kirche',
			'give.call': 'Anrufen',
			'label.accountName': 'Kontoinhaber',
			'label.accountNumber': 'Kontonummer',
			'label.centre': 'Zentrum',
			'footer.follow': 'Folgen Sie uns'
		},
		it: {
			'nav.home': 'Home',
			'nav.about': 'Chi siamo',
			'nav.ministries': 'Ministeri',
			'nav.gallery': 'Galleria',
			'nav.devotional': 'Devozionale quotidiano',
			'nav.announcements': 'Annunci',
			'nav.branches': 'Sedi e trasporti',
			'nav.give': 'Dona',
			'nav.contact': 'Contatti',
			'lang.zambian': 'Lingue zambiane',
			'lang.world': 'Lingue del mondo',
			'lang.select': 'Scegli la lingua',
			'give.subheading': 'Diventa nostro partner',
			'give.title': 'Dona',
			'give.heroLead': 'La tua offerta sostiene l’opera locale, l’ampliamento dell’edificio e la diffusione del Vangelo in Zambia.',
			'give.ways': 'Modi per donare',
			'give.details': 'Dettagli per donare',
			'give.banks': 'Banche zambiane',
			'give.banksLead': 'Dona direttamente su uno dei nostri conti bancari zambiani. Indica il tuo nome come causale, così la chiesa potrà riconoscere la tua offerta.',
			'give.paypal': 'Donazioni internazionali',
			'give.paypalLead': 'Dona dall’estero? Usa il nostro unico gateway internazionale, PayPal.',
			'give.paypalButton': 'Dona con PayPal',
			'give.help': 'Per assistenza su questi dati, contatta l’ufficio della chiesa.',
			'give.email': 'Scrivi alla chiesa',
			'give.call': 'Chiama',
			'label.accountName': 'Intestatario del conto',
			'label.accountNumber': 'Numero di conto',
			'label.centre': 'Centro',
			'footer.follow': 'Seguici'
		},
		pt: {
			'nav.home': 'Início',
			'nav.about': 'Sobre',
			'nav.ministries': 'Ministérios',
			'nav.gallery': 'Galeria',
			'nav.devotional': 'Devocional diário',
			'nav.announcements': 'Anúncios',
			'nav.branches': 'Filiais e transporte',
			'nav.give': 'Ofertar',
			'nav.contact': 'Contacto',
			'lang.zambian': 'Línguas zambianas',
			'lang.world': 'Línguas do mundo',
			'lang.select': 'Escolher idioma',
			'give.subheading': 'Seja nosso parceiro',
			'give.title': 'Ofertar',
			'give.heroLead': 'A sua oferta apoia o trabalho local, a ampliação do edifício e a divulgação do Evangelho na Zâmbia.',
			'give.ways': 'Formas de ofertar',
			'give.details': 'Dados para ofertar',
			'give.banks': 'Bancos zambianos',
			'give.banksLead': 'Ofereça diretamente numa das nossas contas bancárias zambianas. Indique o seu nome como referência para que a igreja possa reconhecer a sua oferta.',
			'give.paypal': 'Ofertas internacionais',
			'give.paypalLead': 'Está a ofertar fora da Zâmbia? Utilize o nosso único gateway internacional, o PayPal.',
			'give.paypalButton': 'Ofertar com PayPal',
			'give.help': 'Para ajuda com estes dados, contacte o escritório da igreja.',
			'give.email': 'Enviar e-mail à igreja',
			'give.call': 'Ligar',
			'label.accountName': 'Nome da conta',
			'label.accountNumber': 'Número da conta',
			'label.centre': 'Centro',
			'footer.follow': 'Siga-nos'
		},
		ru: {
			'nav.home': 'Главная',
			'nav.about': 'О нас',
			'nav.ministries': 'Служения',
			'nav.gallery': 'Галерея',
			'nav.devotional': 'Ежедневное чтение',
			'nav.announcements': 'Объявления',
			'nav.branches': 'Отделения и транспорт',
			'nav.give': 'Пожертвовать',
			'nav.contact': 'Контакты',
			'lang.zambian': 'Замбийские языки',
			'lang.world': 'Языки мира',
			'lang.select': 'Выбрать язык',
			'give.subheading': 'Станьте нашим партнёром',
			'give.title': 'Пожертвовать',
			'give.heroLead': 'Ваше пожертвование поддерживает местное служение, расширение здания и распространение Евангелия по всей Замбии.',
			'give.ways': 'Способы пожертвовать',
			'give.details': 'Реквизиты для пожертвований',
			'give.banks': 'Замбийские банки',
			'give.banksLead': 'Пожертвуйте напрямую на любой из наших счетов в замбийских банках. Укажите своё имя в назначении платежа, чтобы церковь могла отметить ваше пожертвование.',
			'give.paypal': 'Международные пожертвования',
			'give.paypalLead': 'Жертвуете из-за пределов Замбии? Используйте наш единственный международный платёжный сервис — PayPal.',
			'give.paypalButton': 'Пожертвовать через PayPal',
			'give.help': 'По вопросам об этих реквизитах обращайтесь в офис церкви.',
			'give.email': 'Написать в церковь',
			'give.call': 'Позвонить',
			'label.accountName': 'Название счёта',
			'label.accountNumber': 'Номер счёта',
			'label.centre': 'Центр',
			'footer.follow': 'Мы в соцсетях'
		},
		es: {
			'nav.home': 'Inicio',
			'nav.about': 'Acerca de',
			'nav.ministries': 'Ministerios',
			'nav.gallery': 'Galería',
			'nav.devotional': 'Devocional diario',
			'nav.announcements': 'Anuncios',
			'nav.branches': 'Sedes y transporte',
			'nav.give': 'Dar',
			'nav.contact': 'Contacto',
			'lang.zambian': 'Idiomas zambianos',
			'lang.world': 'Idiomas del mundo',
			'lang.select': 'Elegir idioma',
			'give.subheading': 'Sé nuestro socio',
			'give.title': 'Dar',
			'give.heroLead': 'Tu ofrenda apoya la labor local, la ampliación del edificio y la difusión del Evangelio en Zambia.',
			'give.ways': 'Formas de dar',
			'give.details': 'Datos para dar',
			'give.banks': 'Bancos zambianos',
			'give.banksLead': 'Da directamente a cualquiera de nuestras cuentas bancarias zambianas. Usa tu nombre como referencia para que la iglesia pueda reconocer tu ofrenda.',
			'give.paypal': 'Donaciones internacionales',
			'give.paypalLead': '¿Das desde fuera de Zambia? Usa nuestra única pasarela internacional, PayPal.',
			'give.paypalButton': 'Dar con PayPal',
			'give.help': 'Para obtener ayuda con estos datos, contacta con la oficina de la iglesia.',
			'give.email': 'Escribir a la iglesia',
			'give.call': 'Llamar',
			'label.accountName': 'Nombre de la cuenta',
			'label.accountNumber': 'Número de cuenta',
			'label.centre': 'Centro',
			'footer.follow': 'Síguenos'
		},
		hi: {
			'nav.home': 'होम',
			'nav.about': 'हमारे बारे में',
			'nav.ministries': 'सेवाएँ',
			'nav.gallery': 'गैलरी',
			'nav.devotional': 'दैनिक भक्ति',
			'nav.announcements': 'घोषणाएँ',
			'nav.branches': 'शाखाएँ और परिवहन',
			'nav.give': 'दान करें',
			'nav.contact': 'संपर्क करें',
			'lang.zambian': 'ज़ाम्बियाई भाषाएँ',
			'lang.world': 'विश्व भाषाएँ',
			'lang.select': 'भाषा चुनें',
			'give.subheading': 'हमारे साथ भागीदार बनें',
			'give.title': 'दान करें',
			'give.heroLead': 'आपका दान स्थानीय सेवा, भवन विस्तार और पूरे ज़ाम्बिया में सुसमाचार के प्रसार में सहायता करता है।',
			'give.ways': 'दान करने के तरीके',
			'give.details': 'दान विवरण',
			'give.banks': 'ज़ाम्बियाई बैंक',
			'give.banksLead': 'हमारे किसी भी ज़ाम्बियाई बैंक खाते में सीधे दान करें। कृपया अपना नाम संदर्भ के रूप में लिखें ताकि चर्च आपके दान को पहचान सके।',
			'give.paypal': 'अंतर्राष्ट्रीय दान',
			'give.paypalLead': 'ज़ाम्बिया के बाहर से दान कर रहे हैं? हमारे एकमात्र अंतर्राष्ट्रीय गेटवे, PayPal का उपयोग करें।',
			'give.paypalButton': 'PayPal के माध्यम से दान करें',
			'give.help': 'इन विवरणों में सहायता के लिए चर्च कार्यालय से संपर्क करें।',
			'give.email': 'चर्च को ईमेल करें',
			'give.call': 'कॉल करें',
			'label.accountName': 'खाता नाम',
			'label.accountNumber': 'खाता संख्या',
			'label.centre': 'केंद्र',
			'footer.follow': 'हमें फॉलो करें'
		},
		bem: {
			'nav.home': 'Kumukulilo',
			'nav.about': 'Pa ifwe',
			'nav.ministries': 'Imilimo ya Lesa',
			'nav.gallery': 'Ifikope',
			'nav.devotional': 'Icipusho ca bushiku',
			'nav.announcements': 'Ifyebo',
			'nav.branches': 'Amasamba no Lwendo',
			'nav.give': 'Ukupeela',
			'nav.contact': 'Ukwishikana',
			'lang.zambian': 'Indimi sha Zambia',
			'lang.world': 'Indimi sha maiko yambi',
			'lang.select': 'Saleni ululimi',
			'give.subheading': 'Tulingile pamo',
			'give.title': 'Ukupeela',
			'give.heroLead': 'Ukupeela kwanu kukwafwa imilimo ya mu cifulo, ukukula kwa ncito, no kufalisha Amashiwi ya Lesa mu Zambia yonse.',
			'give.ways': 'Inshila shakUpeela',
			'give.details': 'Ifyebo fya kUpeela',
			'give.banks': 'Amabanki ya Zambia',
			'give.banksLead': 'Peleelani ku akaunti yabanki yathu ya Zambia. Bomfya ishina lyenu nga cishibilo kuti icipembo cishibe ukupeela kwanu.',
			'give.paypal': 'Ukupeela kwa maiko yambi',
			'give.paypalLead': 'Muli ukupeela ukufuma ku maiko yambi? Bomfyaniko PayPal, inshila yathu yeka ya maiko yambi.',
			'give.paypalButton': 'Peleela na PayPal',
			'give.help': 'Pa bwafwilisho pa fyebo ifi, ishikani ne ofesi ya cipembo.',
			'give.email': 'Tumeni email ku cipembo',
			'give.call': 'Kwaatileni foni',
			'label.accountName': 'Ishina lya akaunti',
			'label.accountNumber': 'Inombolo ya akaunti',
			'label.centre': 'Apakati',
			'footer.follow': 'Tukonkeni'
		},
		nya: {
			'nav.home': 'Kunyumba',
			'nav.about': 'Za ife',
			'nav.ministries': 'Ntchito za Mulungu',
			'nav.gallery': 'Zithunzi',
			'nav.devotional': 'Za tsiku ndi tsiku',
			'nav.announcements': 'Zolengeza',
			'nav.branches': 'Magawo ndi Mayendedwe',
			'nav.give': 'Kupereka',
			'nav.contact': 'Kulumikizana',
			'lang.zambian': 'Zinenero za ku Zambia',
			'lang.world': 'Zinenero za mayiko ena',
			'lang.select': 'Sankhani chinenero',
			'give.subheading': 'Khalani nawo',
			'give.title': 'Kupereka',
			'give.heroLead': 'Kupereka kwanu kumathandizira ntchito zam’deralo, kukulitsa nyumba, ndi kufalitsa Uthenga Wabwino ku Zambia konse.',
			'give.ways': 'Njira zoperekera',
			'give.details': 'Zambiri zoperekera',
			'give.banks': 'Mabanki aku Zambia',
			'give.banksLead': 'Perekani mwachindunji ku akaunti imodzi mwa mabanki athu aku Zambia. Chonde gwiritsani ntchito dzina lanu monga referensi kuti mpingo udziwe kupereka kwanu.',
			'give.paypal': 'Kupereka kwa mayiko ena',
			'give.paypalLead': 'Mukupereka kuchokera kunja kwa Zambia? Gwiritsani ntchito PayPal, njira yathu yokhayo yapadziko lonse.',
			'give.paypalButton': 'Perekani ndi PayPal',
			'give.help': 'Kwa thandizo pa zambiri izi, lumikizanani ndi ofesi ya mpingo.',
			'give.email': 'Tumizani imelo ku mpingo',
			'give.call': 'Imbani foni',
			'label.accountName': 'Dzina la akaunti',
			'label.accountNumber': 'Nambala ya akaunti',
			'label.centre': 'Likulu',
			'footer.follow': 'Titsatireni'
		},
		toi: {
			'nav.home': 'Kumatalikilo',
			'nav.about': 'Za ndiswe',
			'nav.ministries': 'Milingo ya Leza',
			'nav.gallery': 'Zifaniso',
			'nav.devotional': 'Cilongololo ca buzuba',
			'nav.announcements': 'Makani',
			'nav.branches': 'Matabi a Zilwendo',
			'nav.give': 'Kupeela',
			'nav.contact': 'Kutumina',
			'lang.zambian': 'Ndimi zya Zambia',
			'lang.world': 'Ndimi zya matunji amakwabo',
			'lang.select': 'Saleni ndimi',
			'give.subheading': 'Tiyende pamo',
			'give.title': 'Kupeela',
			'give.heroLead': 'Kupeela kwenu kulayalusa milimo ya mucisi, kukula kwa ng’anda, akufalisa Mulumbe Wabotu mu Zambia yonse.',
			'give.ways': 'Nzila zyakupeela',
			'give.details': 'Makani aakupeela',
			'give.banks': 'Mabanki a Zambia',
			'give.banksLead': 'Pelelani ku akaunti yabanki yesu ya Zambia. Ambozya zina lyenu kuti cikombelo cizibe kupeela kwenu.',
			'give.paypal': 'Kupeela kwa matunji amakwabo',
			'give.paypalLead': 'Muli kupeela kufuma kunze kwa Zambia? Ambozya PayPal, nzila yesu yeka ya matunji.',
			'give.paypalButton': 'Pelelani na PayPal',
			'give.help': 'Kwa bwafo pa makani aya, sumbani ku ofesi ya cikombelo.',
			'give.email': 'Tumizyi email ku cikombelo',
			'give.call': 'Iitani foni',
			'label.accountName': 'Zina lya akaunti',
			'label.accountNumber': 'Namba ya akaunti',
			'label.centre': 'Mukati',
			'footer.follow': 'Tutobeleni'
		},
		loz: {
			'nav.home': 'Kwa Hae',
			'nav.about': 'Ka za luna',
			'nav.ministries': 'Misebezi ya Mulimu',
			'nav.gallery': 'Lifaniso',
			'nav.devotional': 'Za lika ni lika',
			'nav.announcements': 'Makande',
			'nav.branches': 'Mafelo ni Lwendo',
			'nav.give': 'Kufa',
			'nav.contact': 'Kukopanya',
			'lang.zambian': 'Dipuo za Zambia',
			'lang.world': 'Dipuo za linaha ze nngwe',
			'lang.select': 'Keta puo',
			'give.subheading': 'Mube baka luna',
			'give.title': 'Kufa',
			'give.heroLead': 'Kufa kwa luna ku kwahilisa misebezi ya mwahae, ku kula kwa ndu, ni ku kalisa Muka Mukwa Mulimu mwa Zambia kaufela.',
			'give.ways': 'Njila za ku fa',
			'give.details': 'Makande a ku fa',
			'give.banks': 'Mabanki a Zambia',
			'give.banksLead': 'Fanga kwa akaunti ye nngwe ya mabanki a luna a Zambia. Kwalisa libizo la luna kuti kereke i zibe kufa kwa luna.',
			'give.paypal': 'Kufa kwa linaha ze nngwe',
			'give.paypalLead': 'Ha u fa ku zwa kwa nze ya Zambia? Sebelisa PayPal, njila ya luna ye nngwe ya linaha.',
			'give.paypalButton': 'Fa ka PayPal',
			'give.help': 'Kwa thuso ya makande a, bukwa ofisi ya kereke.',
			'give.email': 'Lumela kereke ka email',
			'give.call': 'Bizanga foni',
			'label.accountName': 'Libizo la akaunti',
			'label.accountNumber': 'Nambala ya akaunti',
			'label.centre': 'Sentara',
			'footer.follow': 'Lu latele'
		},
		tum: {
			'nav.home': 'Kunyumba',
			'nav.about': 'Za ise',
			'nav.ministries': 'Ntchito za Chiuta',
			'nav.gallery': 'Vithuzi',
			'nav.devotional': 'Vya zuva na zuva',
			'nav.announcements': 'Makani',
			'nav.branches': 'Vigaŵa na Mayendedwe',
			'nav.give': 'Kupereka',
			'nav.contact': 'Kulumikizana',
			'lang.zambian': 'Viyowoyero vya Zambia',
			'lang.world': 'Viyowoyero vya vyaru vinyake',
			'lang.select': 'Sankhani chiyowoyero',
			'give.subheading': 'Tilutenge pamoza',
			'give.title': 'Kupereka',
			'give.heroLead': 'Kupereka kwinu kukovwira ntchito za mu chigawa, kukura kwa nyumba, na kufalitska Uthenga Uwemi mu Zambia yose.',
			'give.ways': 'Njira za kupereka',
			'give.details': 'Uthenga wa kupereka',
			'give.banks': 'Mabanki gha Zambia',
			'give.banksLead': 'Perekani mwacindunji ku akaunti ya banki yithu ya Zambia. Chonde gwiritsani ntchito zina linu nga chizindikiro kuti mpingo uzibe kupereka kwinu.',
			'give.paypal': 'Kupereka kwa vyaru vinyake',
			'give.paypalLead': 'Mukupereka kufuma kunja kwa Zambia? Gwiritsani ntchito PayPal, njira yithu yekha ya vyaru vinyake.',
			'give.paypalButton': 'Perekani na PayPal',
			'give.help': 'Kwa wovwiri pa uthenga uwu, lumikizanani na ofesi ya mpingo.',
			'give.email': 'Tumizgani email ku mpingo',
			'give.call': 'Imbani foni',
			'label.accountName': 'Zina la akaunti',
			'label.accountNumber': 'Nambala ya akaunti',
			'label.centre': 'Pakati',
			'footer.follow': 'Titsatileni'
		}
	};

	var byCode = {};
	LANGUAGES.forEach(function (language) { byCode[language.code] = language; });

	function translate(lang, key) {
		var table = DICTIONARY[lang] || DICTIONARY.en;
		return table[key] || DICTIONARY.en[key] || '';
	}

	function readStored() {
		try {
			return window.localStorage.getItem(STORAGE_KEY);
		} catch (err) {
			return null;
		}
	}

	function store(lang) {
		try {
			window.localStorage.setItem(STORAGE_KEY, lang);
		} catch (err) {
			/* Private mode can refuse storage; the page still translates. */
		}
	}

	function normaliseHref(href) {
		return (href || '').split('#')[0].split('?')[0].replace(/^\.\//, '');
	}

	/* Proper nouns are never handed to the translation engine. */
	function markUntranslatable() {
		var selector = [
			'.rpai-bank-name',
			'.rpai-bank-full-name',
			'.rpai-paypal-word',
			'.rpai-lang-switcher',
			'.site-menu',
			'.site-mobile-menu',
			'.site-logo'
		].join(',');
		document.querySelectorAll(selector).forEach(function (element) {
			element.classList.add('notranslate');
			element.setAttribute('translate', 'no');
		});

		/* The account name is a proper noun; "To be confirmed" and the centre
		   line are ordinary copy, so they still translate. */
		document.querySelectorAll('.rpai-bank-details dd').forEach(function (element) {
			if (/Dunamis International Gospel Centre/i.test(element.textContent)) {
				element.classList.add('notranslate');
				element.setAttribute('translate', 'no');
			}
		});
	}

	function updateSwitcher(lang) {
		document.querySelectorAll('[data-lang]').forEach(function (option) {
			option.setAttribute('aria-selected', option.getAttribute('data-lang') === lang ? 'true' : 'false');
		});

		var current = document.querySelector('[data-rpai-lang-current]');
		if (current) current.textContent = byCode[lang].name;

		var toggle = document.querySelector('[data-rpai-lang-toggle]');
		if (toggle) toggle.setAttribute('aria-label', translate(lang, 'lang.select'));
	}

	/* Translation that works without a network connection: the interface
	   labels and the giving page copy. World languages let the full-page
	   engine translate the body, so only the interface is set here. */
	function applyDictionary(lang, includeContent) {
		document.querySelectorAll('[data-i18n]').forEach(function (element) {
			var inSwitcher = element.closest('[data-rpai-lang-switcher]');
			if (!includeContent && !inSwitcher) return;
			var value = translate(lang, element.getAttribute('data-i18n'));
			if (value) element.textContent = value;
		});

		/* The header menu and the cloned mobile menu share the same routes. */
		document.querySelectorAll('.site-menu a, .site-mobile-menu a').forEach(function (link) {
			var key = NAV_KEYS[normaliseHref(link.getAttribute('href'))];
			if (key) link.textContent = translate(lang, key);
		});
	}

	/* ------------------------------------------------------- Page translator */
	var originalNodes = new Map();
	var originalAttrs = new Map();
	var translationToken = 0;
	var translationCache = {};
	var currentLanguage = 'en';

	var SKIP_SELECTOR = [
		'script', 'style', 'noscript', 'textarea', 'select', 'option',
		'.notranslate', '[translate="no"]'
	].join(',');

	function hasTranslatableText(value) {
		return /[A-Za-z\u00C0-\u024F\u0400-\u04FF\u0900-\u097F]/.test(value || '');
	}

	/* The built-in dictionary is the English source for the giving page, so
	   reset those strings before collecting text to translate. */
	function resetContentToEnglish() {
		document.querySelectorAll('[data-i18n]').forEach(function (element) {
			var english = DICTIONARY.en[element.getAttribute('data-i18n')];
			if (english) element.textContent = english;
		});
	}

	function splitEdges(value) {
		var leading = value.match(/^\s*/)[0];
		var trailing = value.match(/\s*$/)[0];
		return {
			leading: leading,
			text: value.slice(leading.length, value.length - trailing.length),
			trailing: trailing
		};
	}

	/* Every visible string is collected once. The originals are kept so the
	   page can switch languages (or return to English) without a reload. */
	function collectSources() {
		var items = [];
		var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
			acceptNode: function (node) {
				if (!hasTranslatableText(node.nodeValue)) return NodeFilter.FILTER_REJECT;
				var parent = node.parentElement;
				if (!parent || parent.closest(SKIP_SELECTOR)) return NodeFilter.FILTER_REJECT;
				return NodeFilter.FILTER_ACCEPT;
			}
		});
		var node;
		while ((node = walker.nextNode())) {
			if (!originalNodes.has(node)) originalNodes.set(node, node.nodeValue);
			items.push({ node: node, source: originalNodes.get(node) });
		}

		document.querySelectorAll('[placeholder], [title], [aria-label]').forEach(function (element) {
			if (element.closest(SKIP_SELECTOR)) return;
			var saved = originalAttrs.get(element) || {};
			['placeholder', 'title', 'aria-label'].forEach(function (attribute) {
				if (!element.hasAttribute(attribute)) return;
				if (!(attribute in saved)) saved[attribute] = element.getAttribute(attribute);
				if (hasTranslatableText(saved[attribute])) {
					items.push({ element: element, attribute: attribute, source: saved[attribute] });
				}
			});
			originalAttrs.set(element, saved);
		});

		return items;
	}

	/* Names and church titles are swapped for private-use characters before
	   translation and put back afterwards, so no engine can translate them. */
	var PROTECTED_TERMS = [
		{ token: '\uE000', text: 'Royal Priesthood Assemblies International' },
		{ token: '\uE001', text: 'Dunamis International Gospel Centre' },
		{ token: '\uE002', text: 'Apostle Dr. Mighty Zunga' },
		{ token: '\uE003', text: 'Mighty Zunga' },
		{ token: '\uE004', text: 'Pastor Thelma' },
		{ token: '\uE005', text: 'Thelma' },
		{ token: '\uE006', text: 'RPAI' }
	];

	function protectTerms(value) {
		PROTECTED_TERMS.forEach(function (term) {
			value = value.split(term.text).join(term.token);
		});
		return value;
	}

	function restoreTerms(value) {
		PROTECTED_TERMS.forEach(function (term) {
			value = value.split(term.token).join(term.text);
		});
		return value;
	}

	function requestTranslation(lang, strings) {
		var joined = protectTerms(strings.join('\n\u241E\n'));
		var url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=' +
			encodeURIComponent(lang) + '&dt=t&q=' + encodeURIComponent(joined);
		return fetch(url).then(function (response) {
			if (!response.ok) throw new Error('Translation request failed');
			return response.json();
		}).then(function (payload) {
			var value = restoreTerms(payload[0].map(function (part) { return part[0]; }).join(''));
			var parts = value.split(/\s*\u241E\s*/);
			return parts.length === strings.length ? parts : null;
		});
	}

	function requestOne(lang, value) {
		return requestTranslation(lang, [value]).then(function (parts) {
			return parts ? parts[0] : null;
		}).catch(function () { return null; });
	}

	function getCache(lang) {
		if (translationCache[lang]) return translationCache[lang];

		var cache = new Map();
		try {
			var raw = window.sessionStorage.getItem('rpai.tr.' + lang);
			if (raw) {
				var saved = JSON.parse(raw);
				Object.keys(saved).forEach(function (key) {
					if (key.length < 1200) cache.set(key, saved[key]);
				});
			}
		} catch (err) {
			/* Private mode or a full store: translate without the cache. */
		}
		translationCache[lang] = cache;
		return cache;
	}

	function saveCache(lang, cache) {
		try {
			var saved = {};
			cache.forEach(function (value, key) {
				if (key.length < 1200) saved[key] = value;
			});
			window.sessionStorage.setItem('rpai.tr.' + lang, JSON.stringify(saved));
		} catch (err) {
			/* The cache is an optimisation only. */
		}
	}

	function buildBatches(unique, cache) {
		var batches = [];
		var batch = [];
		var size = 0;

		unique.forEach(function (value) {
			if (cache.has(value)) return;
			if (batch.length && (size + value.length > 4500 || batch.length >= 120)) {
				batches.push(batch);
				batch = [];
				size = 0;
			}
			batch.push(value);
			size += value.length + 3;
		});
		if (batch.length) batches.push(batch);
		return batches;
	}

	/* Fetch only the strings that are not cached yet. */
	var translationPending = {};
	function ensureTranslations(lang, unique) {
		/* A hover prefetch may still be in flight; join it instead of sending
		   the same strings twice. */
		if (translationPending[lang]) {
			return translationPending[lang].then(function () {
				return ensureTranslations(lang, unique);
			});
		}

		var target = byCode[lang].google;
		var cache = getCache(lang);
		var batches = buildBatches(unique, cache);
		if (!batches.length) return Promise.resolve(cache);

		var request = Promise.all(batches.map(function (group) {
			return requestTranslation(target, group).then(function (parts) {
				if (parts) {
					return group.map(function (value, index) {
						return { source: value, translated: parts[index] };
					});
				}
				/* A changed separator means the batch cannot be split safely;
				   translate its strings one by one instead. */
				return Promise.all(group.map(function (value) {
					return requestOne(target, value).then(function (translated) {
						return { source: value, translated: translated };
					});
				}));
			}).catch(function () {
				return group.map(function (value) {
					return { source: value, translated: null };
				});
			});
		})).then(function (results) {
			results.forEach(function (group) {
				group.forEach(function (pair) {
					if (pair.translated) cache.set(pair.source, pair.translated);
				});
			});
			saveCache(lang, cache);
			return cache;
		});

		translationPending[lang] = request;
		return request.then(function (cache) {
			delete translationPending[lang];
			return cache;
		}, function (err) {
			delete translationPending[lang];
			throw err;
		});
	}

	function translatePage(lang) {
		var token = ++translationToken;
		if (!originalNodes.size && !originalAttrs.size) resetContentToEnglish();

		var items = collectSources();
		var byText = new Map();
		items.forEach(function (item) {
			var edge = splitEdges(item.source);
			if (!edge.text || !hasTranslatableText(edge.text)) return;
			if (!byText.has(edge.text)) byText.set(edge.text, []);
			byText.get(edge.text).push(item);
		});

		var unique = Array.from(byText.keys());
		if (!unique.length) return;

		ensureTranslations(lang, unique).then(function (cache) {
			if (token !== translationToken) return;
			items.forEach(function (item) {
				var edge = splitEdges(item.source);
				var translated = cache.get(edge.text);
				if (!translated) return;
				var value = edge.leading + translated + edge.trailing;
				if (item.node) item.node.nodeValue = value;
				else item.element.setAttribute(item.attribute, value);
			});
			markUntranslatable();
		});
	}

	/* Warming a language on hover or keyboard focus makes the eventual click
	   feel instant, because the strings are already in the cache. */
	var prefetching = {};
	function prefetchTranslation(lang) {
		var entry = byCode[lang];
		if (!entry || !entry.google || lang === 'en' || prefetching[lang]) return;
		if (!originalNodes.size && !originalAttrs.size && currentLanguage !== 'en') return;

		prefetching[lang] = true;
		var items = collectSources();
		var unique = [];
		var seen = new Set();
		items.forEach(function (item) {
			var edge = splitEdges(item.source);
			if (!edge.text || !hasTranslatableText(edge.text) || seen.has(edge.text)) return;
			seen.add(edge.text);
			unique.push(edge.text);
		});
		ensureTranslations(lang, unique).then(function () {
			prefetching[lang] = false;
		}, function () {
			prefetching[lang] = false;
		});
	}

	function restoreOriginalText() {
		translationToken++;
		originalNodes.forEach(function (value, node) {
			if (node.isConnected) node.nodeValue = value;
		});
		originalAttrs.forEach(function (saved, element) {
			if (!element.isConnected) return;
			Object.keys(saved).forEach(function (attribute) {
				element.setAttribute(attribute, saved[attribute]);
			});
		});
		originalNodes = new Map();
		originalAttrs = new Map();
	}

	function apply(lang) {
		if (!byCode[lang]) lang = 'en';
		currentLanguage = lang;

		document.documentElement.setAttribute('lang', byCode[lang].htmlLang);
		updateSwitcher(lang);

		var isWorld = byCode[lang].google && lang !== 'en';
		if (!isWorld) restoreOriginalText();

		/* Navigation and the switcher always use the dictionary. Body copy is
		   translated for world languages, and fully dictionary-driven for
		   English and the five Zambian languages. */
		applyDictionary(lang, !isWorld);
		markUntranslatable();

		if (isWorld) translatePage(lang);
	}

	/* --------------------------------------------------------------- Switcher */
	function setup() {
		var switcher = document.querySelector('[data-rpai-lang-switcher]');
		if (!switcher) return;

		var toggle = switcher.querySelector('[data-rpai-lang-toggle]');
		var menu = switcher.querySelector('[data-rpai-lang-menu]');

		switcher.classList.add('notranslate');
		switcher.setAttribute('translate', 'no');
		markUntranslatable();

		function closeMenu() {
			menu.hidden = true;
			switcher.classList.remove('is-open');
			toggle.setAttribute('aria-expanded', 'false');
		}

		function openMenu() {
			menu.hidden = false;
			switcher.classList.add('is-open');
			toggle.setAttribute('aria-expanded', 'true');
			var selected = menu.querySelector('[aria-selected="true"]');
			if (selected) selected.focus();

			/* The three Zambian languages Google supports are warmed as soon
			   as the menu opens, so a tap applies them immediately. */
			['bem', 'nya', 'tum'].forEach(prefetchTranslation);
		}

		toggle.addEventListener('click', function () {
			if (menu.hidden) openMenu();
			else closeMenu();
		});

		/* Hovering or focusing an option starts its translation early. */
		menu.querySelectorAll('[data-lang]').forEach(function (option) {
			var code = option.getAttribute('data-lang');
			option.addEventListener('pointerenter', function () { prefetchTranslation(code); });
			option.addEventListener('focus', function () { prefetchTranslation(code); });
			option.addEventListener('touchstart', function () { prefetchTranslation(code); }, { passive: true });
		});

		menu.addEventListener('click', function (event) {
			var option = event.target.closest('[data-lang]');
			if (!option) return;
			var lang = option.getAttribute('data-lang');
			store(lang);
			closeMenu();
			toggle.focus();
			apply(lang);
		});

		menu.addEventListener('keydown', function (event) {
			var options = Array.prototype.slice.call(menu.querySelectorAll('[data-lang]'));
			var index = options.indexOf(document.activeElement);
			if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
				event.preventDefault();
				var step = event.key === 'ArrowDown' ? 1 : -1;
				var next = (index + step + options.length) % options.length;
				options[next].focus();
			}
		});

		document.addEventListener('click', function (event) {
			if (!switcher.contains(event.target)) closeMenu();
		});

		document.addEventListener('keydown', function (event) {
			if (event.key !== 'Escape' || menu.hidden) return;
			closeMenu();
			toggle.focus();
		});

		window.addEventListener('storage', function (event) {
			if (event.key === STORAGE_KEY && event.newValue) apply(event.newValue);
		});

		var stored = readStored();
		apply(byCode[stored] ? stored : 'en');
	}

	setup();
})();
