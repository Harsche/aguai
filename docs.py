from enum import Enum
import os

import config

data: dict


class DocTypes(Enum):
    CPF = 1
    RG = 2
    Photo = 3
    Birthday_Certificate = 4
    Residence_Certificate = 5
    Scholarship = 6
    Guardian_CPF = 7
    Military_Service = 8
    Medical_Exam = 9


docs_subfolder = {
    DocTypes.RG: 'RG (File responses)',
    DocTypes.Photo: 'Foto (File responses)',
    DocTypes.CPF: 'CPF (File responses)',
    DocTypes.Scholarship: 'Comprovante de escolaridade  (File responses)',
    DocTypes.Birthday_Certificate: 'Certidão de nascimento (File responses)',
    DocTypes.Residence_Certificate: 'Comprovante de residência  (File responses)',
    DocTypes.Guardian_CPF: 'Documento de identidade (File responses)',
    DocTypes.Military_Service: 'Situação de serviço militar (File responses)',
    DocTypes.Medical_Exam: 'Atestado médico (File responses)'
}

docs_suffix = {
    DocTypes.RG: 'RG',
    DocTypes.Photo: 'Foto',
    DocTypes.CPF: 'CPF',
    DocTypes.Scholarship: 'Comprovante de escolaridade_',
    DocTypes.Birthday_Certificate: 'Certidão de nascimento',
    DocTypes.Residence_Certificate: 'Comprovante de residência_',
    DocTypes.Guardian_CPF: 'Documento de identidade',
    DocTypes.Military_Service: 'Situação de serviço militar',
    DocTypes.Medical_Exam: 'Atestado médico'
}


def get_doc_path(doc_type, athlete):
    path = data[config.DATA_DOCS_KEY]
    path += f'/{docs_subfolder[doc_type]}/{athlete.cpf}_{docs_suffix[doc_type]}'
    path = get_doc_extension(path)
    return path


def get_doc_type(doc_requested):
    if doc_requested == 'CPF':
        return DocTypes.CPF
    if doc_requested == 'RG':
        return DocTypes.RG
    if doc_requested == 'FOTO':
        return DocTypes.Photo
    if doc_requested == 'Certidão de Nascimento':
        return DocTypes.Birthday_Certificate
    if doc_requested == 'Comprovante Residência':
        return DocTypes.Residence_Certificate
    if doc_requested == 'Comprovante de Escolaridade':
        return DocTypes.Scholarship
    if doc_requested == 'Certificado de Reservista':
        return DocTypes.Military_Service
    if doc_requested == 'Atestado Médico':
        return DocTypes.Medical_Exam
    return


def is_doc_file(doc_type, athlete):
    path = get_doc_path(doc_type, athlete)
    if not path:
        return False
    return os.path.isfile(path)


def get_doc_extension(path):
    pdf_path = path + '.pdf'
    if os.path.isfile(pdf_path):
        return pdf_path
    jpg_path = path + '.jpg'
    if os.path.isfile(jpg_path):
        return jpg_path
    jpeg_path = path + '.jpeg'
    if os.path.isfile(jpeg_path):
        return jpeg_path
    png_path = path + '.png'
    if os.path.isfile(png_path):
        return png_path
    webp_path = path + '.webp'
    if os.path.isfile(webp_path):
        return webp_path
