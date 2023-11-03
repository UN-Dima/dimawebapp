from typing import Iterable

########################################################################


class Choices:
    """"""

    OCDE = (
        'Ciencias naturales y exactas | Matemáticas | Matemática pura',
        'Ciencias naturales y exactas | Matemáticas | Matemática aplicada',
        'Ciencias naturales y exactas | Matemáticas | Estadística y probabilidad',
        'Ciencias naturales y exactas | Matemáticas | Otras matemáticas',
        'Ciencias naturales y exactas | Ciencias de la computación e información | Ciencias de la computación',
        'Ciencias naturales y exactas | Ciencias de la computación e información | Ciencias de la información y bioinformática ',
        'Ciencias naturales y exactas | Ciencias de la computación e información | Otras ciencias de la computación e información',
        'Ciencias naturales y exactas | Ciencias físicas | Física atómica, molecular y química ',
        'Ciencias naturales y exactas | Ciencias físicas | Física de los materiales condensados',
        'Ciencias naturales y exactas | Ciencias físicas | Física de partículas y campos',
        'Ciencias naturales y exactas | Ciencias físicas | Física nuclear',
        'Ciencias naturales y exactas | Ciencias físicas | Física de los fluidos y plasma',
        'Ciencias naturales y exactas | Ciencias físicas | Óptica ',
        'Ciencias naturales y exactas | Ciencias físicas | Astronomía ',
        'Ciencias naturales y exactas | Ciencias físicas | Otras ciencias físicas',
        'Ciencias naturales y exactas | Ciencias químicas | Química orgánica',
        'Ciencias naturales y exactas | Ciencias químicas | Química inorgánica y nuclear',
        'Ciencias naturales y exactas | Ciencias químicas | Físico-química, ciencia de los polímeros, electroquímica',
        'Ciencias naturales y exactas | Ciencias químicas | Química coloidal',
        'Ciencias naturales y exactas | Ciencias químicas | Química analítica',
        'Ciencias naturales y exactas | Ciencias químicas | Otras ciencias químicas',
        'Ciencias naturales y exactas | Ciencias de la tierra y relacionadas con el medio ambiente | Geociencias multidisciplinaria',
        'Ciencias naturales y exactas | Ciencias de la tierra y relacionadas con el medio ambiente | Mineralogía',
        'Ciencias naturales y exactas | Ciencias de la tierra y relacionadas con el medio ambiente | Paleontología',
        'Ciencias naturales y exactas | Ciencias de la tierra y relacionadas con el medio ambiente | Geoquímica y geofísica',
        'Ciencias naturales y exactas | Ciencias de la tierra y relacionadas con el medio ambiente | Geografía física',
        'Ciencias naturales y exactas | Ciencias de la tierra y relacionadas con el medio ambiente | Geología',
        'Ciencias naturales y exactas | Ciencias de la tierra y relacionadas con el medio ambiente | Vulcanología',
        'Ciencias naturales y exactas | Ciencias de la tierra y relacionadas con el medio ambiente | Ciencias medioambientales ',
        'Ciencias naturales y exactas | Ciencias de la tierra y relacionadas con el medio ambiente | Meteorología y ciencias atmosféricas',
        'Ciencias naturales y exactas | Ciencias biológicas | Biología celular, microbiología',
        'Ciencias naturales y exactas | Ciencias biológicas | Virología',
        'Ciencias naturales y exactas | Ciencias biológicas | Bioquímica y biología molecular ',
        'Ciencias naturales y exactas | Ciencias biológicas | Métodos de investigación en bioquímica',
        'Ciencias naturales y exactas | Ciencias biológicas | Micología',
        'Ciencias naturales y exactas | Ciencias biológicas | Biofísica',
        'Ciencias naturales y exactas | Ciencias biológicas | Genética y herencia ',
        'Ciencias naturales y exactas | Ciencias biológicas | Biología reproductiva ',
        'Ciencias naturales y exactas | Ciencias biológicas | Biología del desarrollo',
        'Ciencias naturales y exactas | Otras ciencias naturales y exactas | Otras ciencias naturales y exactas',
        'Ingenierías y tecnologías | Ingeniería civil | Ingeniería civil',
        'Ingenierías y tecnologías | Ingeniería civil | Ingeniería arquitectónica',
        'Ingenierías y tecnologías | Ingeniería civil | Ingeniería de la construcción',
        'Ingenierías y tecnologías | Ingeniería civil | Ingeniería estructural',
        'Ingenierías y tecnologías | Ingeniería civil | Ingeniería del transporte',
        'Ingenierías y tecnologías | Ingeniería civil | Otras ingeniería civil',
        'Ingenierías y tecnologías | Ingeniería eléctrica, ingeniería electrónica e ingeniería de la información | Ingeniería eléctrica y electrónica',
        'Ingenierías y tecnologías | Ingeniería eléctrica, ingeniería electrónica e ingeniería de la información | Control automático y robótica',
        'Ingenierías y tecnologías | Ingeniería eléctrica, ingeniería electrónica e ingeniería de la información | Sistemas de automatización y control',
        'Ingenierías y tecnologías | Ingeniería eléctrica, ingeniería electrónica e ingeniería de la información | Ingeniería de sistemas y comunicaciones',
        'Ingenierías y tecnologías | Ingeniería eléctrica, ingeniería electrónica e ingeniería de la información | Telecomunicaciones',
        'Ingenierías y tecnologías | Ingeniería eléctrica, ingeniería electrónica e ingeniería de la información | Hardware y arquitectura de computadoras',
        'Ingenierías y tecnologías | Ingeniería eléctrica, ingeniería electrónica e ingeniería de la información | Otras ingeniería eléctrica, ingeniería electrónica e ingeniería de la información',
        'Ingenierías y tecnologías | Ingeniería mecánica | Ingeniería mecánica',
        'Ingenierías y tecnologías | Ingeniería mecánica | Mecánica aplicada',
        'Ingenierías y tecnologías | Ingeniería mecánica | Termodinámica',
        'Ingenierías y tecnologías | Ingeniería mecánica | Ingeniería aeroespacial',
        'Ingenierías y tecnologías | Ingeniería mecánica | Ingeniería nuclear ',
        'Ingenierías y tecnologías | Ingeniería mecánica | Ingeniería de audio, análisis de confiabilidad',
        'Ingenierías y tecnologías | Ingeniería mecánica | Otras ingeniería mecánica',
        'Ingenierías y tecnologías | Ingeniería química | Ingeniería química ',
        'Ingenierías y tecnologías | Ingeniería química | Ingeniería de procesos químicos',
        'Ingenierías y tecnologías | Ingeniería química | Otras ingeniería química',
        'Ingenierías y tecnologías | Ingeniería de los materiales | Ingeniería de los materiales',
        'Ingenierías y tecnologías | Ingeniería de los materiales | Cerámicos',
        'Ingenierías y tecnologías | Ingeniería de los materiales | Recubrimientos y películas',
        'Ingenierías y tecnologías | Ingeniería de los materiales | Compuestos ',
        'Ingenierías y tecnologías | Ingeniería de los materiales | Papel y madera',
        'Ingenierías y tecnologías | Ingeniería de los materiales | Textiles ',
        'Ingenierías y tecnologías | Ingeniería de los materiales | Otras ingeniería de los materiales',
        'Ingenierías y tecnologías | Ingeniería médica | Ingeniería médica',
        'Ingenierías y tecnologías | Ingeniería médica | Tecnología de laboratorios médicos ',
        'Ingenierías y tecnologías | Ingeniería médica | Otras ingeniería médica',
        'Ingenierías y tecnologías | Ingeniería del medio ambiente | Ingeniería medioambiental y geológica, geotécnicas',
        'Ingenierías y tecnologías | Ingeniería del medio ambiente | Ingeniería del petróleo, energía y combustibles',
        'Ingenierías y tecnologías | Ingeniería del medio ambiente | Sensores remotos',
        'Ingenierías y tecnologías | Ingeniería del medio ambiente | Minería y procesamiento mineral',
        'Ingenierías y tecnologías | Ingeniería del medio ambiente | Ingeniería marina, ingeniería naval',
        'Ingenierías y tecnologías | Ingeniería del medio ambiente | Ingeniería oceanográfica',
        'Ingenierías y tecnologías | Ingeniería del medio ambiente | Otras ingeniería del medio ambiente',
        'Ingenierías y tecnologías | Biotecnología del medio ambiente | Biotecnología medioambiental',
        'Ingenierías y tecnologías | Biotecnología del medio ambiente | Bioremediación, diagnóstico biotecnológico en gestión medioambiental ',
        'Ingenierías y tecnologías | Biotecnología del medio ambiente | Ética relacionada con biotecnología medioambiental',
        'Ingenierías y tecnologías | Biotecnología del medio ambiente | Otras biotecnología del medio ambiente',
        'Ingenierías y tecnologías | Biotecnología industrial | Biotecnología industrial',
        'Ingenierías y tecnologías | Biotecnología industrial | Bioprocesamiento tecnológico, biocatálisis, fermentación',
        'Ingenierías y tecnologías | Biotecnología industrial | Bioproductos, biomateriales, bioplásticos, biocombustibles, bioderivados, etc.',
        'Ingenierías y tecnologías | Biotecnología industrial | Otras biotecnología industrial',
        'Ingenierías y tecnologías | Biotecnología industrial | Nanotecnología',
        'Ingenierías y tecnologías | Biotecnología industrial | Otras ingenierías y tecnologías',
        'Ciencias médicas y de la salud | Medicina básica | Anatomía y morfología ',
        'Ciencias médicas y de la salud | Medicina básica | Genética humana',
        'Ciencias médicas y de la salud | Medicina básica | Inmunología',
        'Ciencias médicas y de la salud | Medicina básica | Neurociencias ',
        'Ciencias médicas y de la salud | Medicina básica | Farmacología y farmacia',
        'Ciencias médicas y de la salud | Medicina básica | Medicina química',
        'Ciencias médicas y de la salud | Medicina básica | Toxicología',
        'Ciencias médicas y de la salud | Medicina básica | Fisiología ',
        'Ciencias médicas y de la salud | Medicina básica | Patología',
        'Ciencias médicas y de la salud | Medicina clínica | Andrología',
        'Ciencias médicas y de la salud | Medicina clínica | Obstetricia y ginecología',
        'Ciencias médicas y de la salud | Medicina clínica | Pediatría',
        'Ciencias médicas y de la salud | Medicina clínica | Sistemas cardíaco y cardiovascular',
        'Ciencias médicas y de la salud | Medicina clínica | Enfermedades vasculares periféricas',
        'Ciencias médicas y de la salud | Medicina clínica | Hematología',
        'Ciencias médicas y de la salud | Medicina clínica | Sistema respiratorio',
        'Ciencias médicas y de la salud | Medicina clínica | Medicina critica y de emergencia',
        'Ciencias médicas y de la salud | Medicina clínica | Anestesiología',
        'Ciencias médicas y de la salud | Ciencias de la salud | Ciencias y servicios de cuidado de la salud ',
        'Ciencias médicas y de la salud | Ciencias de la salud | Políticas y servicios de salud',
        'Ciencias médicas y de la salud | Ciencias de la salud | Enfermería',
        'Ciencias médicas y de la salud | Ciencias de la salud | Nutrición, dietética',
        'Ciencias médicas y de la salud | Ciencias de la salud | Salud pública y medioambiental',
        'Ciencias médicas y de la salud | Ciencias de la salud | Medicina tropical',
        'Ciencias médicas y de la salud | Ciencias de la salud | Parasitología',
        'Ciencias médicas y de la salud | Ciencias de la salud | Enfermedades infecciosas',
        'Ciencias médicas y de la salud | Ciencias de la salud | Epidemiología',
        'Ciencias médicas y de la salud | Biotecnología de la salud | Biotecnología relacionada con la salud',
        'Ciencias médicas y de la salud | Biotecnología de la salud | Tecnologías que involucran la manipulación de células, tejidos, órganos o todo el organismo ',
        'Ciencias médicas y de la salud | Biotecnología de la salud | Tecnologías que involucran la identificación de adn, proteínas y enzimas, y cómo influyen en el conjunto de enfermedades y mantenimiento del bienestar',
        'Ciencias médicas y de la salud | Biotecnología de la salud | Biomateriales ',
        'Ciencias médicas y de la salud | Biotecnología de la salud | Ética relacionada con biotecnología médica',
        'Ciencias médicas y de la salud | Biotecnología de la salud | Otras biotecnologías de la salud',
        'Ciencias médicas y de la salud | Otras ciencias médicas | Medicina forense',
        'Ciencias médicas y de la salud | Otras ciencias médicas | Otras ciencias médicas',
        'Ciencias agrícolas | Agricultura, silvicultura y pesca | Agricultura',
        'Ciencias agrícolas | Agricultura, silvicultura y pesca | Silvicultura',
        'Ciencias agrícolas | Agricultura, silvicultura y pesca | Pesca',
        'Ciencias agrícolas | Agricultura, silvicultura y pesca | Ciencias del suelo',
        'Ciencias agrícolas | Agricultura, silvicultura y pesca | Horticultura, viticultura',
        'Ciencias agrícolas | Agricultura, silvicultura y pesca | Agronomía, reproducción y protección de plantas ',
        'Ciencias agrícolas | Agricultura, silvicultura y pesca | Otras agricultura, silvicultura y pesca',
        'Ciencias agrícolas | Producción animal y lechería | Producción animal y lechería ',
        'Ciencias agrícolas | Producción animal y lechería | Ganadería',
        'Ciencias agrícolas | Producción animal y lechería | Mascotas',
        'Ciencias agrícolas | Producción animal y lechería | Otras producción animal y lechería',
        'Ciencias agrícolas | Ciencias veterinarias | Ciencias veterinarias',
        'Ciencias agrícolas | Ciencias veterinarias | Otras ciencias veterinarias',
        'Ciencias agrícolas | Biotecnología agropecuaria | Biotecnología agrícola y biotecnología alimentaria',
        'Ciencias agrícolas | Biotecnología agropecuaria | Tecnología gm, clonación de ganado, selección asistida, diagnósticos, tecnología de producción de biomasa, etc.',
        'Ciencias agrícolas | Biotecnología agropecuaria | Ética relacionada con biotecnología agrícola',
        'Ciencias agrícolas | Biotecnología agropecuaria | Otras biotecnología agropecuaria',
        'Ciencias agrícolas | Otras ciencias agrícolas | Otras ciencias agrícolas',
        'Ciencias sociales | Psicología | Psicología ',
        'Ciencias sociales | Psicología | Psicología especial ',
        'Ciencias sociales | Psicología | Otras psicología',
        'Ciencias sociales | Economía y negocios | Economía, econometría',
        'Ciencias sociales | Economía y negocios | Organización industrial',
        'Ciencias sociales | Economía y negocios | Negocios y administración',
        'Ciencias sociales | Economía y negocios | Otras economía y negocios',
        'Ciencias sociales | Ciencias de la educación | Educación general ',
        'Ciencias sociales | Ciencias de la educación | Educación especial ',
        'Ciencias sociales | Ciencias de la educación | Otras ciencias de la educación',
        'Ciencias sociales | Sociología | Sociología',
        'Ciencias sociales | Sociología | Demografía',
        'Ciencias sociales | Sociología | Antropología, etnología',
        'Ciencias sociales | Sociología | Tópicos sociales ',
        'Ciencias sociales | Sociología | Otras sociología',
        'Ciencias sociales | Derecho | Derecho',
        'Ciencias sociales | Derecho | Otras derecho',
        'Ciencias sociales | Ciencia política | Ciencia política',
        'Ciencias sociales | Ciencia política | Administración pública',
        'Ciencias sociales | Ciencia política | Teoría organizacional',
        'Ciencias sociales | Ciencia política | Otras ciencia política',
        'Ciencias sociales | Geografía económica y social | Ciencias medioambientales ',
        'Ciencias sociales | Geografía económica y social | Geografía cultural y económica',
        'Ciencias sociales | Geografía económica y social | Estudios urbanos ',
        'Ciencias sociales | Geografía económica y social | Planeamiento y aspectos sociales del transporte ',
        'Ciencias sociales | Geografía económica y social | Otras geografía económica y social',
        'Ciencias sociales | Comunicación y medios | Periodismo',
        'Ciencias sociales | Comunicación y medios | Bibliotecología',
        'Ciencias sociales | Comunicación y medios | Comunicación de medios y socio-cultural',
        'Ciencias sociales | Comunicación y medios | Otras comunicación y medios',
        'Ciencias sociales | Otras ciencias sociales | Ciencias sociales interdisciplinarias',
        'Ciencias sociales | Otras ciencias sociales | Otras ciencias sociales',
        'Humanidades | Historia y arqueología | Historia ',
        'Humanidades | Historia y arqueología | Arqueología',
        'Humanidades | Historia y arqueología | Otras historia y arqueología',
        'Humanidades | Lengua y literatura | Estudios generales del lenguaje',
        'Humanidades | Lengua y literatura | Lenguajes específicos',
        'Humanidades | Lengua y literatura | Estudios generales de literatura',
        'Humanidades | Lengua y literatura | Teoría literaria',
        'Humanidades | Lengua y literatura | Literaturas específicas',
        'Humanidades | Lengua y literatura | Lingüística',
        'Humanidades | Lengua y literatura | Otras lengua y literatura',
        'Humanidades | Filosofía, ética y religión | Filosofía, historia y filosofía de la ciencia y la tecnología',
        'Humanidades | Filosofía, ética y religión | Ética ',
        'Humanidades | Filosofía, ética y religión | Teología',
        'Humanidades | Filosofía, ética y religión | Estudios religiosos',
        'Humanidades | Filosofía, ética y religión | Otras filosofía, étnica y religión',
        'Humanidades | Arte | Arte, historia del arte',
        'Humanidades | Arte | Diseño arquitectónico',
        'Humanidades | Arte | Artes escénicas ',
        'Humanidades | Arte | Estudios del folklore',
        'Humanidades | Arte | Estudios sobre cine, radio y televisión',
        'Humanidades | Arte | Otras artes',
        'Humanidades | Otras humanidades | Otras humanidades',
    )

    KNOWLEDGE = (
        'Ambiente y biodiversidad',
        'Arte y cultura',
        'Biotecnología',
        'Ciencia y tecnología de minerales y materiales',
        'Ciencias agrarias y desarrollo rural',
        'Construcción de ciudadanía e inclusión social',
        'Desarrollo organizacional, económico e industrial',
        'Energía',
        'Estados, sistemas políticos y jurídicos',
        'Hábitat, ciudad y territorio',
        'Salud y vida',
        'Tecnologías de la información y las comunicaciones',
    )

    DEPARTAMENT = (
        'Departamento de Administración',
        'Departamento de Ciencias Humanas',
        'Departamento de Física y Química',
        'Departamento de Informática y Computación',
        'Departamento de Ingeniería Civil',
        'Departamento de Ingeniería Eléctrica, Electrónica y Computación',
        'Departamento de Ingeniería Industrial',
        'Departamento de Ingeniería Química',
        'Departamento de Matemáticas',
        'Escuela de Arquitectura y Urbanismo',
        'Otro'
        # 'Instituto de estudios ambientales - idea - manizales'
    )

    FACULTY = (
        'Facultad de Administración',
        'Facultad de Ciencias Exactas y Naturales',
        'Facultad de Ingeniería y Arquitectura',
        'Sin Información',
        # 'Instituto de estudios ambientales - idea - manizales'
    )

    RESEARCHER_CATEGORY = (
        'Investigador Asociado',
        'Investigador Emérito',
        'Investigador Junior',
        'Investigador Senior',
        'Sin categoría'
    )

    RESEARCHER_CATEGORY_SORTED = (
        'Sin categoría',
        'Investigador Junior',
        'Investigador Asociado',
        'Investigador Senior',
        'Investigador Emérito'
    )

    GROUPS_CATEGORY = (
        'A1',
        'A',
        'B',
        'C',
        'No reconocido',
    )

    CALL_TYPE = (
        'Externa',
        'Interna',
        'Minciencias',
        'Otra',
        'Regalías',
    )

    CALL_STATE = (
        'Abierta',
        'Finalizada'
    )

    CALL_STUDENT = (
        'Posgrado'
        'Pregrado',
    )

    PROJECT_STATE = (
        'Activo',
        'Finalizado',
        'No aprobado',
        'Propuesto',
        'Sin finalizar',
        'Suspendido',
    )

    PATENT_TYPE = (
        'Patente de invención',
        'Patente modelo de utilidad',
    )
    DEDICATION = (
        'Docente catedra 0,3', 'Docente catedra 0,4',
        'Docente catedra 0,5', 'Docente catedra 0,6',
        'Docente catedra 0,7', 'Docente dedicac. exclusiva',
        'Docente medio tiempo', 'Docente tiempo completo',
    )

    

    # ----------------------------------------------------------------------
    def __new__(self, choices: str) -> dict:
        """"""
        assert getattr(
            self, choices, False), f"Choices for '{choices}' not found."

        n = 4
        prefix = choices.lower()
        choices = sorted(list(set(getattr(self, choices))))
        choices = [(f'{prefix}_{str(i).rjust(n, "0")}', choice)
                   for i, choice in enumerate(choices, start=1)]

        return {'max_length': len(choices[0][0]) + 100, 'choices': choices, }

