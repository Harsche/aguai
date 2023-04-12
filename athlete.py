import os.path
import docs
from docs import DocTypes
from PIL import Image, ImageTk
import io
import os
import shutil
import pdf_compressor


class Athlete:
    def __init__(self, athlete_dict, data):
        self.name: str = athlete_dict['Nome completo do(a) atleta'].strip()
        self.nickname: str = athlete_dict['Apelido'].strip()
        self.motherName: str = athlete_dict['Nome completo da mãe']
        self.fatherName: str = athlete_dict['Nome completo do pai']
        self.birthday: str = athlete_dict['Data de nascimento']
        self.isMinor = athlete_dict['Menor de idade'] == 'Sim'
        self.gender: str = athlete_dict['Sexo biológico']
        self.cpf: str = str(athlete_dict['CPF']).strip().zfill(11)
        self.rg: str = str(athlete_dict['RG.1']).strip()
        self.email: str = athlete_dict['Email'].strip()
        self.civilState: str = athlete_dict['Estado civil']
        self.scholarship: str = athlete_dict['Grau de instrução ']
        self.countryBorn: str = athlete_dict['País de origem']
        self.stateBorn: str = athlete_dict['UF de Naturalidade']
        self.cityBorn: str = str(athlete_dict['Cidade de Naturalidade']).strip()
        self.guardianName: str = athlete_dict['Nome completo do responsável']
        self.guardianPhone: str = athlete_dict['Telefone de contato do responsável']
        self.guardianCpf: str = athlete_dict['CPF.1']
        self.doc_guardianCpf = docs.get_doc_path(DocTypes.Guardian_CPF, self, data)
        self.doc_photo = docs.get_doc_path(DocTypes.Photo, self, data)
        self.doc_rg = docs.get_doc_path(DocTypes.RG, self, data)
        self.doc_cpf = docs.get_doc_path(DocTypes.CPF, self, data)
        if not self.doc_cpf or not os.path.isfile(self.doc_cpf):
            self.doc_cpf = self.doc_rg
        self.doc_scholarship = docs.get_doc_path(DocTypes.Scholarship, self, data)
        self.doc_birthCertificate = docs.get_doc_path(DocTypes.Birthday_Certificate, self, data)
        self.doc_residenceCertificate_ = docs.get_doc_path(DocTypes.Residence_Certificate, self, data)
        self.doc_militaryService = docs.get_doc_path(DocTypes.Military_Service, self, data)
        self.doc_medicalExam = docs.get_doc_path(DocTypes.Medical_Exam, self, data)
        self.cep: str = athlete_dict['CEP']
        self.addressStreet: str = athlete_dict['Nome da rua']
        self.addressNum: str = athlete_dict['Número']
        self.addressComplement: str = athlete_dict['Complemento']
        self.addressNeighbourhood: str = athlete_dict['Bairro']
        self.addressState: str = athlete_dict['UF']
        self.addressCity: str = str(athlete_dict['Cidade']).strip()

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
        if doc_type == DocTypes.Medical_Exam:
            return self.doc_medicalExam
        return None

    def compress_files(self):
        # Convert png to jpg
        files = [self.doc_photo, self.doc_rg, self.doc_cpf, self.doc_scholarship, self.doc_guardianCpf,
                 self.doc_residenceCertificate_, self.doc_militaryService, self.doc_medicalExam,
                 self.doc_birthCertificate]

        for i in range(len(files)):
            path = files[i]
            if path and ('.png' in path or '.webp' in path) and os.path.isfile(path):
                png = Image.open(path)
                png = png.convert('RGB')
                new_path = path.replace('.png', '.jpg')
                new_path = new_path.replace('.webp', '.jpg')
                png.save(new_path)
                os.remove(path)
                files[i] = new_path

            # Compress images
        for i in range(len(files)):
            path = files[i]
            if not path:
                continue
            if '.jpg' in path:
                compress_image(path, 500)
                continue
            if '.pdf' in path:
                compress_pdf(path, 500)


def compress_image(file_path, max_size_kb):
    max_size_bytes = max_size_kb * 1024
    # Open the image file
    img = Image.open(file_path)
    quality = img.info.get('quality', 100)
    # Check if the file is larger than 500kB
    while True:
        # Reduce the JPEG quality by 10%
        quality -= 10
        img.save(file_path, 'JPEG', quality=quality, optimize=True, progressive=True)

        # Check the resulting file size
        file_size = os.path.getsize(file_path)

        # If the file size is less than the target size, break the loop
        if file_size <= max_size_bytes:
            break

        # If the quality falls below 30, stop compressing
        if quality <= 30:
            break


def compress_pdf(path, max_size_kb):
    max_size_bytes = max_size_kb * 1024
    if os.path.getsize(path) < max_size_bytes:
        return
    copy_path = path.replace('_', '@')
    shutil.copy(path, copy_path)
    pdf_compressor.compress(copy_path, path, 3)
    os.remove(copy_path)
