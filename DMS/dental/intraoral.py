class Tooth():
    def __init__(self, toothcolors, status1, status2):
        self.toothcolors = toothcolors
        self.status1 = status1
        self.ststus2 = status2






    def asd():
        pass


legend = {
    # Condition
    '/':'Present Teeth',
    'D':'Decayed Teeth',
    'M':'Missing (Caries Indicated for Filling)',
    'MO':'Missing Due to Caries',
    'Im':'Impacted Tooth',
    'Sp':'Supernumerary Tooth',
    'Rf':'Root Fragment',
    'Un':'Unerupted',
    # Restorations & Prosthetics
    'Am':'Amaigam Filling',
    'Co':'Composite Filling',
    'JC':'Jacket Crown',
    'Ab':'Abutment',
    'Att':'Attatchment',
    'P':'Pontic',
    'In':'Inlay',
    'Imp':'Implant',
    'S':'Sealants',
    'Rm':'Removable Denture',
    # Surgery
    'X':'Extraction due to Caries',
    'XO':'Extraction due to Other Causes',
}


tooth11 = Tooth([],)





# FOR MODELS AND FORMS IN INTRAORAL EXAMINATION

# FOR FORMS XRAY
xray = [
    ('',''),
    ('',''),
    ('',''),
    ('',''),
]





#  CLASS THAT IS BETTER FOR COUPLING WITH DJANGO AND JSON
# class Tooth:
#     def __init__(self, tooth_number, toothcolors, status1, status2):
#         self.tooth_number = tooth_number
#         self.toothcolors = toothcolors
#         self.status1 = status1
#         self.status2 = status2

#     def __str__(self):
#         return f"Tooth {self.tooth_number} with colors {self.toothcolors} and status1: {self.status1}, status2: {self.status2}"



# Example of creating an IntraoralExamination with teeth: THIS IS WRONG SINCE THERE ARE NO SPECIFIC COLORS FOR TOP LEFT MIDDLE RIGHT BOTTOM teeth sections 

# exam = IntraoralExamination.objects.create(
#     patient=patient_instance,
#     teeth=[
#         {"tooth": "11", "color": ["white"], "status1": "Healthy", "status2": "No issues"},
#         {"tooth": "12", "color": ["red"], "status1": "Cavity", "status2": "Requires filling"},
#         {"tooth": "13", "color": ["blue"], "status1": "Healthy", "status2": "No issues"},
#     ]
# )