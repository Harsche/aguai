# Selenium webdriver files
GECKODRIVER_PATH = r'""geckodriver\geckodriver.exe""'
# FIREFOX_PROFILE_PATH = r'C:\Users\henri\AppData\Roaming\Mozilla\Firefox\Profiles\nescs7tq.default'


# region CBF

# Login XPaths
LOGIN_EMAIL_XPATH = '/html/body/table/tbody/tr/td/form/table/tbody/tr/td[3]/div/input[1]'
LOGIN_PASSWORD_XPATH = '/html/body/table/tbody/tr/td/form/table/tbody/tr/td[3]/div/input[2]'
LOGIN_BUTTON_XPATH = '/html/body/table/tbody/tr/td/form/table/tbody/tr/td[3]/div/input[3]'

# Registration Xpaths
CPF_FIELD_XPATH = '//*[@id="cpf"]'
NAME_FIELD_XPATH = '//*[@id="atletaNomeCompleto"]'
NICKNAME_FIELD_XPATH = '//*[@id="apelido"]'
BIRTHDAY_FIELD_XPATH = '//*[@id="dataNascimento"]'
GENDER_FIELD_XPATH = '//*[@id="sexo"]'
CIVIL_STATE_FIELD_XPATH = '//*[@id="codigoEstadoCivil"]'
SCHOLARSHIP_FIELD_XPATH = '//*[@id="grau_instrucao"]'
FATHER_NAME_FIELD_XPATH = '//*[@id="nomePai"]'
MOTHER_NAME_FIELD_XPATH = '//*[@id="nomeMae"]'
COUNTRY_BORN_FIELD_XPATH = '//*[@id="codigoNacionalidade"]'
STATE_BORN_FIELD_XPATH = '//*[@id="naturalidadeUf"]'
CITY_BORN_FIELD_XPATH = '//*[@id="naturalidade"]'
EMAIL_FIELD_XPATH = '//*[@id="email"]'
CONFIRMATION_EMAIL_FIELD_XPATH = '//*[@id="emailConfirmacao"]'
NEXT_BUTTON_XPATH = '/html/body/div[3]/div[2]/div[2]/div/form/div/div[4]/div/div/div[1]/a[3]'
DOC_TYPE_DROPDOWN_XPATH = '//*[@id="idTipoDocumento"]'
ADD_DOC_BUTTON_XPATH = '//*[@id="btn-add-documento"]'
CEP_FIELD_XPATH = '//*[@id="cep"]'
ADDRESS_STREET_FIELD_XPATH = '//*[@id="enderecoResidencial"]'
ADDRESS_NUMBER_FIELD_XPATH = '//*[@id="numero"]'
ADDRESS_COMPLEMENT_FIELD_XPATH = '//*[@id="complemento"]'
ADDRESS_NEIGHBOURHOOD_FIELD_XPATH = '//*[@id="bairro"]'
ADDRESS_STATE_DROPDOWN_XPATH = '//*[@id="estado"]'
ADDRESS_CITY_DROPDOWN_XPATH = '//*[@id="codigoMunicipio"]'

# Athlete List Xpaths
CODE_DROPDOWN_XPATH = '//*[@id="campoBusca"]'
CPF_SEARCH_FIELD_XPATH = '//*[@id="busca"]'
SEARCH_BUTTON_XPATH = '/html/body/div[3]/div[2]/div[2]/div/div/form/div[1]/div/div/button'
ACTIONS_ATHLETE_BUTTON_XPATH = '/html/body/div[3]/div[2]/div[2]/div/div/form/table/tbody/tr/td[10]/div/a'
EDIT_ATHLETE_BUTTON_XPATH = '/html/body/div[3]/div[2]/div[2]/div/div/form/table/tbody/tr/td[10]/div/ul/li[1]/a'
EDIT_GUARDIAN_BUTTON_XPATH = '/html/body/div[3]/div[2]/div[2]/div/div/form/table/tbody/tr/td[10]/div/ul/li[3]/a'
EDIT_CONTRACT_BUTTON_XPATH = '/html/body/div[3]/div[2]/div[2]/div/div/form/table/tbody/tr/td[10]/div/ul/li[2]/a'
EDIT_NEXT_BUTTON_XPATH = '/html/body/div[3]/div[2]/div[2]/div[1]/form/div/div[5]/div/div[1]/a[3]'
EDIT_SELECT_DOC_TYPE_XPATH = '/html/body/div[3]/div[2]/div[2]/div[1]/form/div/div[5]/div/div[2]/div[2]/div[2]/div[3]/div/table/tbody/tr[index]/td[2]'
EDIT_SELECT_DOC_BUTTON_XPATH = '/html/body/div[3]/div[2]/div[2]/div[1]/form/div/div[5]/div/div[2]/div[2]/div[2]/div[3]/div/table/tbody/tr[index]/td[7]/div/a'
EDIT_SET_FILE_FIELD_XPATH = '//*[@id="arquivo"]'
EDIT_SEND_FILE_BUTTON_XPATH = '/html/body/div[3]/div[2]/div[2]/div[9]/div[3]/a'

# Anthropometry Xpaths
SHIRT_DROPDOWN = '//*[@id="material_camisa"]'
BLOUSE_DROPDOWN = '//*[@id="material_agasalho"]'
PANTS_DROPDOWN = '//*[@id="material_calca"]'
SHORT_DROPDOWN = '//*[@id="material_short"]'
SHOES_DROPDOWN = '//*[@id="material_calcado"]'

# Guardian Xpaths
GUARDIAN_CPF_FIELD = '//*[@id="documentoCpf"]'
GUARDIAN_CPF_SEARCH_BUTTON = '/html/body/div[3]/div[2]/div[2]/div/form/div/div[4]/div/div/div/div[1]/div[1]/div/button'
GUARDIAN_IS_PARENT_DROPDOWN = '//*[@id="isPai"]'
GUARDIAN_ACTIVE_DROPDOWN = '//*[@id="Codigo_Situacao"]'
GUARDIAN_DOC_FILE_FIELD = '//*[@id="documento_comprovatorio"]'
GUARDIAN_SAVE_BUTTON = '//*[@id="btnSalvar"]'

# Contract Xpaths
CONTRACT_TICKET_BUTTON = '//*[@id="btnGerarBoleto"]'
CONTRACT_TICKET_TYPE_DROPDOWN = '//*[@id="idTipoContratoBoleto"]'
CONTRACT_FINALIZE_BUTTON = '/html/body/div[3]/div[2]/div[2]/div/form/div[7]/div[3]/a'
CONTRACT_NEW_BUTTON = '//*[@id="btnNovoContrato"]'
CONTRACT_DAYS_FIELD = '//*[@id="diasAmador"]'
CONTRACT_START_DATE_FIELD = '//*[@id="dataInicioAmador"]'
CONTRACT_NEXT_1_BUTTON = '/html/body/div[3]/div[2]/div[2]/div/form/div[12]/div[2]/ul/li[2]/a'
CONTRACT_NEXT_2_BUTTON = '/html/body/div[3]/div[2]/div[2]/div/form/div[12]/div[2]/ul/li[3]/a'
CONTRACT_DOCTOR_DROPDOWN = '//*[@id="idPessoaMedicoAmador"]'
CONTRACT_EXAM_BUTTON = '/html/body/div[3]/div[2]/div[2]/div/form/div[12]/div[2]/div/div[2]/div[3]/div[1]/ul/li/label/input'
CONTRACT_EXAM2_BUTTON = '/html/body/div[3]/div[2]/div[2]/div/form/div[12]/div[2]/div/div[2]/div[3]/div[2]/ul/li[2]/label/input'
CONTRACT_EXAM3_BUTTON = '/html/body/div[3]/div[2]/div[2]/div/form/div[12]/div[2]/div/div[2]/div[3]/div[2]/ul/li[3]/label/input'
CONTRACT_EXAM_DATE_FIELD = '//*[@id="dataAtestadoAmador"]'
CONTRACT_SAVE_BUTTON = '/html/body/div[3]/div[2]/div[2]/div/form/div[12]/div[2]/div/div[3]/div[3]/div/button'

# IDs
CHECK_LOGGED_ID = 'btn-busca-global-atleta'

# URLs
NEW_ATHLETE_URL = 'https://gestaoweb.cbf.com.br/site/registro/atleta/adicionar/'
CBF_LOGIN_URL = 'https://gestaoweb.cbf.com.br/site/login/page/'
ATHLETE_LIST_URL = 'https://gestaoweb.cbf.com.br/site/registro/atleta/listar/'
ATHLETE_CONTRACT_URL = 'https://gestaoweb.cbf.com.br/site/registro/atleta/contrato/'
# endregion


# region FPF

# URLs FPF
FPF_LOGIN_URL = 'https://portaldoclube.fpf.org.br/'
FPF_NEW_ATHLETE_URL = 'https://extranetclube.fpf.org.br/NovoAtleta.aspx'
FPF_ATHLETE_REGISTER_URL = 'https://extranetclube.fpf.org.br/RegistroAtleta.aspx'

# Login Xpaths
FPF_LOGIN_PATH = '//*[@id="email"]'
FPF_PASSWORD_PATH = '//*[@id="password"]'
FPF_LOGIN_BUTTON_PATH = '//*[@id="btnLogin"]'

# New Athlete
FPF_HOMEPAGE = '/html/body/div[3]/ul/li[1]'
FPF_AUTH_DROPDOWN = '/html/body/div[3]/ul/li[3]/a'
FPF_AUTH_REGISTER = '/html/body/div[3]/ul/li[3]/ul/li[3]/a'

FPF_NEW_ATHLETE_BUTTON = '//*[@id="__tab_TabContainer1_TabPanel1"]'
FPF_NEW_ATHLETE_CPF_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel1_txtCpf"]'
FPF_NEW_ATHLETE_GO_BUTTON = '//*[@id="TabContainer1_TabPanel1_btChecarCpfAtleta"]'
FPF_NAME_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel1_txtNomeAtleta"]'
FPF_NICKNAME_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel1_txtApelidoAtleta"]'
FPF_FATHER_NAME_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel1_txtNomePai"]'
FPF_MOTHER_NAME_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel1_txtNomeMae"]'
FPF_BIRTHDAY_INPUT_FIELD = '//*[@id="txtDtNascimento"]'
FPF_GENDER_DROPDOWN = '//*[@id="TabContainer1_TabPanel1_DropDwSexo"]'
FPF_BIRTH_STATE_DROPDOWN = '//*[@id="TabContainer1_TabPanel1_DropDwEstadoNatural"]'
FPF_BIRTH_CITY_DROPDOWN = '//*[@id="TabContainer1_TabPanel1_DropDwMuniNatural"]'
FPF_RG_INPUT_FIELD = '//*[@id="txtRg"]'
FPF_RG_ORG_DROPDOWN = '//*[@id="TabContainer1_TabPanel1_DropDwOrgEmis"]'
FPF_BIRTH_CERT_NUM_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel1_txtNumCertidao"]'
FPF_BIRTH_CERT_PAGE_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel1_txtCertFolha"]'
FPF_BIRTH_CERT_BOOK_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel1_txtCertLivro"]'
FPF_MILITARY_CERT_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel1_txtCertMilitar"]'
FPF_CTPS_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel1_txtCtps"]'
FPF_GRADE_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel1_txtSerie"]'
FPF_CEP_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel1_txtCepAtleta"]'
FPF_STREET_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel1_txtEnderecoAtleta"]'
FPF_HOUSE_NUM_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel1_txtNumero"]'
FPF_COMPLEMENT_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel1_txtComplemento"]'
FPF_NEIGHBOURHOOD_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel1_txtBairro"]'
FPF_STATE_DROPDOWN = '//*[@id="TabContainer1_TabPanel1_DropDownEst"]'
FPF_CITY_DROPDOWN = '//*[@id="TabContainer1_TabPanel1_DropDownMun"]'
FPF_NEW_ATHLETE_SAVE_BUTTON = '//*[@id="TabContainer1_TabPanel1_btSalvarDados"]'

FPF_SEARCH_CPF_INPUT_FIELD = '//*[@id="TabContainer1_TabPanel2_txtCpfFiltro"]'
FPF_SEARCH_CPF_BUTTON = '//*[@id="TabContainer1_TabPanel2_btFiltrar"]'
FPF_SEARCH_EDIT_BUTTON = '/html/body/form/div[6]/div[1]/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div/div/table/tbody/tr[2]/td[4]/input'
FPF_UPDATE_ATHLETE_BUTTON = '//*[@id="TabContainer1_TabPanel1_btUpdateAtleta"]'
FPF_UPDATE_ATHLETE_DOCS_BUTTON = '//*[@id="TabContainer1_TabPanel1_btRedirectArquivos"]'

# Docs

FPF_PHOTO_INPUT_FILE = '//*[@id="fileUplFotoAtleta"]'
FPF_PHOTO_SEND_BUTTON = '//*[@id="btEnviarFotoAtl"]'
FPF_RG_INPUT_FILE = '//*[@id="fileUplFotoRg"]'
FPF_RG_SEND_BUTTON = '//*[@id="btEnviarFotoRg"]'
FPF_CPF_INPUT_FILE = '//*[@id="FileUploadcpf"]'
FPF_CPF_SEND_BUTTON = '//*[@id="btEnviarFotoCpf"]'
FPF_GUARDIAN_DOC_INPUT_FILE = '//*[@id="FileUploadDocResp"]'
FPF_GUARDIAN_SEND_BUTTON = '//*[@id="btEnviarDocResponsavel"]'
FPF_HEALTH_EXAM_INPUT_FILE = '//*[@id="FileUploadAtestadoMedico"]'
FPF_HEALTH_EXAM_SEND_BUTTON = '//*[@id="btEnviarAtestadoMedico"]'
FPF_BIRTH_CERT_INPUT_FILE = '//*[@id="fileUplFotoCrtNasc"]'
FPF_BIRTH_CERT_SEND_BUTTON = '//*[@id="btEnviarFotoCrtNasc"]'
FPF_MILITARY_SERV_INPUT_FILE = '//*[@id="fileUplFotoMilitar"]'
FPF_MILITARY_SERV_SEND_BUTTON = '//*[@id="btEnviarFotoMilitar"]'
FPF_SCHOLARSHIP_INPUT_FILE = '//*[@id="fileUplFotoHistEsc"]'
FPF_SCHOLARSHIP_SEND_BUTTON = '//*[@id="btEnviarFotoHistEsc"]'
FPF_ADDRESS_INPUT_FILE = '//*[@id="FileUpFotoCompEnd"]'
FPF_ADDRESS_SEND_BUTTON = '//*[@id="btEnviarFotoCompEndereco"]'

# Contract

FPF_CONTRACT_CPF_INPUT_FIELD = '//*[@id="txtCpf"]'
FPF_CONTRACT_CPF_SEARCH_BUTTON = '//*[@id="btBuscaAtleta"]'
FPF_CONTRACT_TYPE_DROPDOWN = '//*[@id="DropDownListTipoNome"]'
FPF_CONTRACT_SEND_BUTTON = '//*[@id="btEnviar"]'
FPF_CONTRACT_FINALIZE_BUTTON = '//*[@id="btFinalizarProcesso"]'
FPF_CONTRACT_FINALIZE_CONFIRM = '//*[@id="lblFinalizarInfo"]'

# Doctor

FPF_FORM_SELECT_ATHLETE = '/html/body/form/div[9]/div[1]/div[1]/div[1]/div[5]/div/div/table/tbody/tr[2]/td[8]/a/img'
FPF_FORM_EDIT = '/html/body/form/div[9]/div/div[1]/div[1]/div[2]/div/div[1]/table/tbody/tr[2]/td[4]/input'
FPF_DOCTOR_NAME_INPUT_FIELD = '//*[@id="txtNomeMedico"]'
FPF_DOCTOR_CRM_INPUT_FIELD = '//*[@id="txtCrmMedico"]'
FPF_DOCTOR_CPF_INPUT_FIELD = '//*[@id="txtCpfMedico"]'
FPF_GENERATE_FORM_BUTTON = '//*[@id="btGerarForm"]'

# endregion


# DATA
DATA_FORMS_KEY = 'formPath'
DATA_DOCS_KEY = 'docsPath'
DATA_LOGIN_CBF_KEY = 'loginCBF'
DATA_PASSWORD_CBF_KEY = 'passwordCBF'
DATA_LOGIN_FPF_KEY = 'loginFPF'
DATA_PASSWORD_FPF_KEY = 'passwordFPF'
