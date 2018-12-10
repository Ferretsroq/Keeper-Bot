import PyPDF2 as pdf
import json

class Chosen:
    def __init__(self, manifest, sheetFields):
        self.manifest = manifest
        self.fields = {}
        for field in sheetFields:
            if('/V' in sheetFields[field]):
                self.fields[field] = sheetFields[field]['/V']
        self.moves = [self.manifest[move] for move in self.fields if move.startswith('move')]
        self.moves.append(self.manifest['move5'])
        self.moves.append(self.manifest['move6'])
        self.weapon = self.SetWeapon()
        self.harm = len([field for field in self.fields if field.startswith('harm')])
        self.luck = len([field for field in self.fields if field.startswith('luck')])
        self.charm = self.fields['charm']
        self.cool = self.fields['cool']
        self.sharp = self.fields['sharp']
        self.tough = self.fields['tough']
        self.weird = self.fields['weird']
        
    def __repr__(self):
        reprString = ''
        for field in self.fields:
            if(field in self.manifest):
                reprString += '{}: {}\n'.format(field, self.manifest[field])
            else:
                reprString += '{}: {}\n'.format(field, self.fields[field])
        return reprString
    def __getitem__(self, key):
        if(key in self.fields and key in self.manifest):
            return self.manifest[key]
        elif(key in self.fields):
            return self.fields[key]
    def SetWeapon(self):
        forms = [form for form in self.fields if form.startswith('form')]
        if(forms != []):
            form = forms[0] # Only allowed to have one form
        ends = [end for end in self.fields if end.startswith('end')][0:3]
        harm = 0
        tags = []
        name = ''
        endNames = []
        if(form == 'form0'):
            name = 'staff'
            harm += 1
            tags.append('hand/close')
        elif(form == 'form1'):
            name = 'haft'
            harm += 2
            tags.append('hand')
            tags.append('heavy')
        elif(form == 'form2'):
            name = 'handle'
            harm += 1
            tags.append('hand')
            tags.append('balanced')
        elif(form == 'form3'):
            name = 'chain'
            harm += 1
            tags.append('hand')
            tags.append('area')
        if('end0' in ends):
            endNames.append('artifact')
            tags.append('magic')
        if('end1' in ends):
            endNames.append('spikes')
            harm += 1
            tags.append('messy')
        if('end2' in ends):
            endNames.append('blade')
            harm += 1
        if('end3' in ends):
            endNames.append('heavy')
            harm += 1
        if('end4' in ends):
            endNames.append('long')
            tags.append('close')
        if('end5' in ends):
            endNames.append('thorwable')
            tags.append('close')
        if('end6' in ends):
            endNames.append('chain')
            tags.append('area')
        tags.append('{}-harm'.format(harm))
        return '**{} {}** form with {} ({})'.format(self.fields['material'].title(), name.title(), ', '.join(endNames), ', '.join(tags))
        
def Load():
	sheetPath = './Character Stuff/Demo Characters/'
	fieldPath = './Character Stuff/Field Data/'
	pdfFileObj = open(sheetPath+'The_Chosen.pdf', 'rb')
	pdfReader = pdf.PdfFileReader(pdfFileObj)
	fields = pdfReader.getFields()
	fieldData = open(fieldPath+'Chosen Fields.json')
	data = json.load(fieldData)
	fieldData.close()
	pdfFileObj.close()
	return Chosen(data, fields)