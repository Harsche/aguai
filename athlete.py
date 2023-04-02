import os.path
import docs
from docs import DocTypes


class Athlete:
    def __init__(self, athlete_dict, data):
        self.name: str = athlete_dict['Nome completo do(a) atleta'].strip()
        self.nickname: str = athlete_dict['Apelido'].strip()
        self.motherName: str = athlete_dict['Nome completo da mãe']
        self.fatherName: str = athlete_dict['Nome completo do pai']
        self.birthday: str = athlete_dict['Data de nascimento']
        self.isMinor = athlete_dict['Menor de idade'] == 'Sim'
        self.gender: str = athlete_dict['Sexo biológico']
        self.cpf: str = athlete_dict['CPF'].strip()
        self.email: str = athlete_dict['Email'].strip()
        self.civilState: str = athlete_dict['Estado civil']
        self.scholarship: str = athlete_dict['Grau de instrução ']
        self.countryBorn: str = athlete_dict['País de origem']
        self.stateBorn: str = athlete_dict['UF de Naturalidade']
        self.cityBorn: str = athlete_dict['Cidade de Naturalidade']
        self.guardianName: str = athlete_dict['Nome completo do responsável']
        self.guardianPhone: str = athlete_dict['Telefone de contato do responsável']
        self.guardianCpf: str = athlete_dict['CPF.1']
        self.doc_guardianCpf = docs.get_doc_path(DocTypes.Guardian_CPF, self, data)
        self.doc_photo = docs.get_doc_path(DocTypes.Photo, self, data)
        self.doc_rg = docs.get_doc_path(DocTypes.RG, self, data)
        self.doc_cpf = docs.get_doc_path(DocTypes.CPF, self, data)
        if not os.path.isfile(self.doc_cpf):
            self.doc_cpf = self.doc_rg
        self.doc_scholarship = docs.get_doc_path(DocTypes.Scholarship, self, data)
        self.doc_birthCertificate = docs.get_doc_path(DocTypes.Birthday_Certificate, self, data)
        self.doc_residenceCertificate_ = docs.get_doc_path(DocTypes.Residence_Certificate, self, data)
        self.doc_militaryService = docs.get_doc_path(DocTypes.Military_Service, self, data)
        self.cep: str = athlete_dict['CEP']
        self.addressStreet: str = athlete_dict['Nome da rua']
        self.addressNum: str = athlete_dict['Número']
        self.addressComplement: str = athlete_dict['Complemento']
        self.addressNeighbourhood: str = athlete_dict['Bairro']
        self.addressState: str = athlete_dict['UF']
        self.addressCity: str = athlete_dict['Cidade']

    def get_doc_path(self, doc_type):
        if doc_type == DocTypes.CPF:
            return self.doc_cpf
        if doc_type == DocTypes.RG:
            return self.doc_rg
        if doc_type == DocTypes.Photo:
            return self.doc_photo
        if doc_type == DocTypes.Birthday_Certificate:
            return self.doc_birthCertificate
        if doc_type == DocTypes.Residence_Certificate:
            return self.doc_residenceCertificate_
        if doc_type == DocTypes.Scholarship:
            return self.doc_scholarship
        if doc_type == DocTypes.Guardian_CPF:
            return self.doc_guardianCpf
        if doc_type == DocTypes.Military_Service:
            return self.doc_militaryService
        return None
