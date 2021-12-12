import os
import re
import traceback
import PySimpleGUI as sg

factionlist = []
globalfactionlist = []
faction_found = 0
mesh_found = 0
notexture = 0
factiondict = {}
modeldict = {}
modellist = []
upgmodellist = []
unitlist = []
officer_dict = {}
upgmodel_dict = {}
merc_dict = {}
unitmount_dict = {}
unit_found = 0
mountdict = {}
unit_ctgdict = {}
culturedict = {}
culturelist = []
religiondict = {}
religionlist = []
sslist = []
nocardlist = []

currentpath = os.getcwd()
modpath = currentpath

sg.set_options(background_color='#002740',
        text_element_background_color='#002740',
        element_background_color='#002740',
        scrollbar_color='#780000',
        input_elements_background_color='#454242',
        button_color=('white','#454242'),
        text_color='#ffffff',
        element_text_color='#ffffff',
        input_text_color='#ffffff')
        

layout =                [   [sg.Text('Select path to mod: ')],
                            [sg.Input(default_text=modpath, size=(100, 1), key='modpath'), sg.FolderBrowse()],
                            [sg.Text('Ignored factions (separate with comma): '), sg.Input(default_text='', size=(100, 1), key='ignoredfactions')],
                            [sg.Text('Ignored models (separate with comma): '), sg.Input(default_text='', size=(100, 1), key='ignoredmodels')],
                            [sg.Text('Ignored units (separate with comma): '), sg.Input(default_text='', size=(100, 1), key='ignoredunits')],
                            [sg.Checkbox('Include results from EDU ownership? ', k = 'enableownership', default=True)],
                            [sg.Button('Check mod', border_width=(3), button_color='#455642', tooltip="Press after selecting a folder or typing a path to confirm, select the modfolder of the mod you want to use"), sg.Button('Quit', border_width=(3), button_color='#780000')]
]

window = sg.Window('Medieval 2 Silver Surfer Checker', layout, finalize=True, resizable=True)

def EncodeFinder(file, filename):
    encodings = ['utf8', 'cp1252', 'cp1250']
    for i in encodings:
        try:
            file = open(filename, 'r', encoding=i)
            file.readlines()
            file.seek(0)
            return file
            break
        except UnicodeDecodeError:
            continue

def CheckSilverSurfer(unit, faction, file, line, modeltype, factype, set_card, set_info):
    try:
        if faction != 'scripts' and faction not in ignored_factionslist and unit_ctgdict[unit] != 'ship' and unit not in ignored_unitslist:
            if modeltype == 'unit':
                if set_card == 0:
                    if merc_dict[unit] == 1:
                        if dicname_dict[unit].lower().strip() not in unit_cards['merc']: 
                            entrycheck = unit+"merc"
                            if entrycheck not in nocardlist:
                                outputfile.write("Unit: " + unit + " "  + dicname_dict[unit].lower().strip() + " " + "#mercenary_unit attribute! " + " ### No unit card!" + "\n")
                                #print(dicname_dict[unit].lower().strip(), (unit_cards['merc']), "merc")
                                nocardlist.append(entrycheck) 
                    elif factype == 'faction' and merc_dict[unit] == 0:
                        if dicname_dict[unit].lower().strip() not in unit_cards[faction]:
                            entrycheck = unit+faction
                            if entrycheck not in nocardlist:
                                outputfile.write("Unit: " + unit + " " + dicname_dict[unit].lower().strip() + " " + " #Faction: " + faction + " ### No unit card!"  + "\n" )
                                #print(dicname_dict[unit].lower().strip(), (unit_cards[faction]), faction)
                                nocardlist.append(entrycheck)
                    elif factype == 'culture' and merc_dict[unit] == 0:
                        for cfaction in culturedict[faction]:
                            if dicname_dict[unit].lower().strip() not in unit_cards[cfaction]:
                                entrycheck = unit+cfaction
                                if entrycheck not in nocardlist:
                                    outputfile.write("Unit: " + unit + " "  + dicname_dict[unit].lower().strip() + " " + " #Faction: " + cfaction + " ### No unit card!" + "\n")
                                    #print(dicname_dict[unit].lower().strip(), (unit_cards[faction]), cfaction)
                                    nocardlist.append(entrycheck)   
                if set_info == 0:
                    if merc_dict[unit] == 1:
                        if dicname_dict[unit].lower().strip() not in info_cards['merc']: 
                            entrycheck = unit+"merc"+"info"
                            if entrycheck not in nocardlist:
                                outputfile.write("Unit: " + unit + " "  + dicname_dict[unit].lower().strip() + " " + "#mercenary_unit attribute! " + " ### No unit info card!" + "\n")
                                #print(dicname_dict[unit].lower().strip(), (unit_cards['merc']), "merc")
                                nocardlist.append(entrycheck) 
                    elif factype == 'faction' and merc_dict[unit] == 0:
                        if dicname_dict[unit].lower().strip() not in info_cards[faction]:
                            entrycheck = unit+faction+"info"
                            if entrycheck not in nocardlist:
                                outputfile.write("Unit: " + unit + " " + dicname_dict[unit].lower().strip() + " " + " #Faction: " + faction + " ### No unit info card!" + "\n" )
                                #print(dicname_dict[unit].lower().strip(), (unit_cards[faction]), faction)
                                nocardlist.append(entrycheck)
                    elif factype == 'culture' and merc_dict[unit] == 0:
                        for cfaction in culturedict[faction]:
                            if dicname_dict[unit].lower().strip() not in info_cards[cfaction]:
                                entrycheck = unit+cfaction+"info"
                                if entrycheck not in nocardlist:
                                    outputfile.write("Unit: " + unit + " "  + dicname_dict[unit].lower().strip() + " " + " #Faction: " + cfaction + " ### No unit info card!" + "\n")
                                    #print(dicname_dict[unit].lower().strip(), (unit_cards[faction]), cfaction)
                                    nocardlist.append(entrycheck)  
                if len(officer_dict[unit]) > 0:
                    for officer in officer_dict[unit]:
                        if merc_dict[unit] == 1:
                            if officer not in factiondict['merc']:
                                entrycheck = unit+"merc"+officer
                                if entrycheck not in sslist and officer not in ignored_modelslist:
                                    outputfile.write("Unit: " + unit  + " " + "#mercenary_unit attribute! " + " #Model: "  + officer + " #On Line "  + str(line) + " in "  + file + " ### Officer model" + "\n")
                                    sslist.append(entrycheck)
                        elif merc_dict[unit] == 0:
                            if factype == 'culture':
                                for cfaction in culturedict[faction]:
                                    if officer not in factiondict[cfaction]:
                                        entrycheck = unit+cfaction+officer
                                        if entrycheck not in sslist and cfaction not in ignored_factionslist and officer not in ignored_modelslist:
                                            outputfile.write("Unit: " + unit  + " " + " #Faction: " + cfaction + " "+ " #Model: "  + officer + " #On Line "  + str(line) + " in "  + file + " ### Officer model" + "\n")
                                            sslist.append(entrycheck)
                            elif factype == 'religion':
                                for rfaction in religiondict[faction]:
                                    if officer not in factiondict[rfaction]:
                                        entrycheck = unit+rfaction+officer
                                        if entrycheck not in sslist and rfaction not in ignored_factionslist and officer not in ignored_modelslist:
                                            outputfile.write("Unit: " + unit  + " " + " #Faction: " + rfaction + " "+ " #Model: "  + officer + " #On Line "  + str(line) + " in "  + file + " ### Officer model" + "\n")
                                            sslist.append(entrycheck)
                            elif factype == 'faction':
                                if officer not in factiondict[faction]:
                                    entrycheck = unit+faction+officer
                                    if entrycheck not in sslist and officer not in ignored_modelslist:
                                        outputfile.write("Unit: " + unit  + " " + " #Faction: " + faction + " "+ " #Model: "  + officer + " #On Line "  + str(line) + " in "  + file + " ### Officer model" + "\n")
                                        sslist.append(entrycheck)
                for model in upgmodel_dict[unit]:
                    if merc_dict[unit] == 1:
                        if model not in factiondict['merc']:
                            entrycheck = unit+"merc"+model
                            if entrycheck not in sslist and model not in ignored_modelslist:
                                outputfile.write("Unit: " + unit  + " " + "#mercenary_unit attribute! " + " #Model: "  + model + " #On Line "  + str(line) + " in "  + file + "\n")
                                sslist.append(entrycheck)
                    elif merc_dict[unit] == 0:
                        if factype == 'culture':
                            for cfaction in culturedict[faction]:
                                if model not in factiondict[cfaction]:
                                    entrycheck = unit+cfaction+model
                                    if entrycheck not in sslist and cfaction not in ignored_factionslist and model not in ignored_modelslist:
                                        outputfile.write("Unit: " + unit  + " " + " #Faction: " + cfaction + " "+ " #Model: "  + model + " #On Line "  + str(line) + " in "  + file + "\n") 
                                        sslist.append(entrycheck)
                        elif factype == 'religion':
                            for rfaction in religiondict[faction]:
                                if model not in factiondict[rfaction]:
                                    entrycheck = unit+rfaction+model
                                    if entrycheck not in sslist and rfaction not in ignored_factionslist and model not in ignored_modelslist:
                                        outputfile.write("Unit: " + unit  + " " + " #Faction: " + rfaction + " "+ " #Model: "  + model + " #On Line "  + str(line) + " in "  + file + "\n") 
                                        sslist.append(entrycheck)
                        elif factype == 'faction':
                            if model not in factiondict[faction]:
                                entrycheck = unit+faction+model
                                if entrycheck not in sslist and model not in ignored_modelslist:
                                    outputfile.write("Unit: " + unit  + " " + " #Faction: " + faction + " "+ " #Model: "  + model + " #On Line "  + str(line) + " in "  + file + "\n") 
                                    sslist.append(entrycheck)
                try:
                    mountmodel = mountdict[unitmount_dict[unit]]
                    if merc_dict[unit] == 1:
                        if mountmodel not in factiondict['merc']:
                            entrycheck = unit+"merc"+mountmodel
                            if entrycheck not in sslist and mountmodel not in ignored_modelslist:
                                outputfile.write("Unit: " + unit  + " " + "#mercenary_unit attribute! " + " #Model: "  + mountmodel + " #On Line "  + str(line) + " in "  + file + " ### Mount" + "\n")
                                sslist.append(entrycheck)
                    elif merc_dict[unit] == 0:          
                        if factype == 'culture':
                            for cfaction in culturedict[faction]:
                                if mountmodel not in factiondict[cfaction]:
                                    entrycheck = unit+cfaction+mountmodel
                                    if entrycheck not in sslist and cfaction not in ignored_factionslist and mountmodel not in ignored_modelslist:
                                        outputfile.write("Unit: " + unit  + " " + " #Faction: " + cfaction + " "+ " #Model: "  + mountmodel + " #On Line "  + str(line) + " in "  + file + " ### Mount" + "\n")  
                                        sslist.append(entrycheck)
                        elif factype == 'religion':
                            for rfaction in religiondict[faction]:
                                if mountmodel not in factiondict[rfaction]:
                                    entrycheck = unit+rfaction+mountmodel
                                    if entrycheck not in sslist and rfaction not in ignored_factionslist and mountmodel not in ignored_modelslist:
                                        outputfile.write("Unit: " + unit  + " " + " #Faction: " + rfaction + " "+ " #Model: "  + mountmodel + " #On Line "  + str(line) + " in "  + file + " ### Mount" + "\n")  
                                        sslist.append(entrycheck)
                        elif factype == 'faction':
                            if mountmodel not in factiondict[faction]:
                                entrycheck = unit+faction+mountmodel
                                if entrycheck not in sslist and mountmodel not in ignored_modelslist:
                                    outputfile.write("Unit: " + unit  + " " + " #Faction: " + faction + " "+ " #Model: "  + mountmodel + " #On Line "  + str(line) + " in "  + file + " ### Mount" + "\n")  
                                    sslist.append(entrycheck)
                except:
                        mountmodel = ""           
            elif modeltype != 'unit':
                if merc_dict[unit] == 0:
                    if modeltype not in factiondict[faction]:
                        entrycheck = unit+faction+modeltype
                        if entrycheck not in sslist and modeltype not in ignored_modelslist:
                            outputfile.write("Unit: " + unit  + " " + " #Faction: " + faction + " "+ " #Model: "  + modeltype + " #On Line "  + str(line) + " in "  + file + " ### General" + "\n")
                            sslist.append(entrycheck)
                if merc_dict[unit] == 1:
                    if modeltype not in factiondict['merc']:
                        entrycheck = unit+"merc"+modeltype
                        if entrycheck not in sslist and modeltype not in ignored_modelslist:
                            outputfile.write("Unit: " + unit  + " " + "#mercenary_unit attribute! " + " #Model: "  + modeltype + " #On Line "  + str(line) + " in "  + file + " ### General" + "\n")
                            sslist.append(entrycheck)
    except:
        print('Something went wrong!, on line ' + str(line) + " in " + file + ' ' + unit + ' ' + faction)

try:
    while True: 
        event, values = window.read()
        
        # -------------------------Quit button-------------------------------------------
        if event == sg.WIN_CLOSED or event == 'Quit':
            break
        
        if event == 'Check mod':
            factionlist = []
            globalfactionlist = []
            faction_found = 0
            mesh_found = 0
            notexture = 0
            factiondict = {}
            modeldict = {}
            modellist = []
            upgmodellist = []
            unitlist = []
            officer_dict = {}
            upgmodel_dict = {}
            merc_dict = {}
            unitmount_dict = {}
            unit_found = 0
            mountdict = {}
            unit_ctgdict = {}
            culturedict = {}
            culturelist = []
            religiondict = {}
            religionlist = []
            dicname_dict = {}
            sslist = []
            nocardlist = []
            if (values['modpath']) != "":
                modpath = values['modpath']

            eduname = modpath + "\\data\\export_descr_unit.txt"
            edbname = modpath + "\\data\\export_descr_buildings.txt"
            bmdbname = modpath + "\\data\\unit_models\\battle_models.modeldb"
            mountsname = modpath + "\\data\\descr_mount.txt"
            smfactionsname = modpath + "\\data\\descr_sm_factions.txt"
            rebelsname = modpath + "\\data\\descr_rebel_factions.txt"
            outputfilename = modpath + "\\silver_surfers.txt"
            dsname = modpath + "\\data\\world\\maps\\campaign\\imperial_campaign\\descr_strat.txt"
            csname = modpath + "\\data\\world\\maps\\campaign\\imperial_campaign\\campaign_script.txt"
            mercname = modpath + "\\data\\world\\maps\\campaign\\imperial_campaign\\descr_mercenaries.txt"

            ignored_factions = values['ignoredfactions']
            ignored_factionslist = ignored_factions.split(',')
            ignored_models = values['ignoredmodels'].lower()
            ignored_modelslist = ignored_models.split(',')
            ignored_units = values['ignoredunits']
            ignored_unitslist = ignored_units.split(',')

            file_edu = EncodeFinder('file_edu', eduname)
            mounts  = EncodeFinder('mounts', mountsname)
            file_cs = EncodeFinder('file_cs', csname)
            file_ds = EncodeFinder('file_ds', dsname)
            file_bmdb = EncodeFinder('file_bmdb', bmdbname)
            file_edb = EncodeFinder('file_edb', edbname)
            file_merc = EncodeFinder('file_merc', mercname)
            file_rebels = EncodeFinder('file_rebels', rebelsname)
            file_smfactions = EncodeFinder('file_bmdb', smfactionsname)
            outputfile = open(outputfilename, 'w') 

            file_smfactions.seek(0)
            for line in file_smfactions:
                if re.search(r'^;', line) is not None:
                    continue
                if re.search(r';', line) is not None:
                    line = line.split(';')[0]
                if re.search(r'^faction', line) is not None:
                    sm_faction = re.findall(r'^faction\s+([:0-z:]+),*', line)[0]
                if re.search(r'^culture', line) is not None:  
                    sm_culture = re.findall(r'^culture\s+([:0-z:]+),*', line)[0]
                    if sm_culture not in culturelist:
                        culturedict[sm_culture] = []
                        culturelist.append(sm_culture)
                    culturedict[sm_culture].append(sm_faction.strip())
                if re.search(r'^religion', line) is not None:  
                    sm_religion = re.findall(r'^religion\s+([:0-z:]+),*', line)[0]
                    if sm_religion not in religionlist:
                        religiondict[sm_religion] = []
                        religionlist.append(sm_religion)
                    religiondict[sm_religion].append(sm_faction.strip())

            file_bmdb.seek(0)
            for line in file_bmdb:
                if re.search(r'\d+\s*([:A-z:].+?)\n', line) is not None and re.search(r'\d+\s*blank', line) is None and re.search(r'\d+\s*serialization::archive\s', line) is None and re.search(r'\.spr', line) is None and re.search(r'\.mesh', line) is None and re.search(r'\.texture', line) is None:
                    modelentrystr = re.findall(r'\d+\s*([:A-z:].+?)\n', line)[0].strip()
                if re.search(r'\.texture', line) is not None:
                    notexture = 0
                if re.search(r'\.texture', line) is None and re.search(r'\.spr', line) is None and mesh_found == 1 and faction_found == 1:
                    notexture += 1
                    if notexture >= 3:
                        mesh_found = 0
                        faction_found = 0
                        modelentry = ""
                        modelentrystr = ""
                        faction = ""
                        notexture = 0
                elif re.search(r'\.mesh', line) is not None:
                    modelentry = modelentrystr
                    mesh_found = 1
                    modeldict[modelentry] = factionlist
                if mesh_found == 1 and re.search(r'\d+\s*([:A-z:].+?)\s', line) is not None and re.search(r'\.spr', line) is None and re.search(r'\.mesh', line) is None and re.search(r'\.texture', line) is None:
                    faction_found = 1
                    faction = re.findall(r'\d+\s*([:A-z:].+?)\s', line)[0]
                    if faction != 'None' and faction != 'Horse' and faction != 'Elephant' and faction != 'Camel':
                        if faction not in globalfactionlist:
                            globalfactionlist.append(faction)
                            factiondict[faction] = modellist
                        if modelentry not in factiondict[faction]:
                            factiondict[faction].append(modelentry.lower())
                        if faction not in modeldict[modelentry]:
                            modeldict[modelentry].append(faction)
                    modellist = []
                    factionlist = []

            culturedict['all'] = globalfactionlist
            religiondict['all'] = globalfactionlist
            #print(religiondict)
                
            mounts.seek(0)
            for line in mounts:
                if re.search(r'^;', line) is not None:
                    continue
                if re.search(r';', line) is not None:
                    line = line.split(';')[0]
                if re.search(r'^type\s', line) is not None:
                    mount_type = re.findall(r'^type\s+(\S.+)', line)[0].strip().lower()
                    mount_found = 1
                if re.search(r'^model\s', line) is not None and mount_found == 1:
                    mountdict[mount_type] = re.findall(r'^model\s+(\S.+)', line)[0].strip().lower()
                    mount_found = 0

            unit_cards = {}
            faction_dir = ""
            for dir in os.listdir(modpath + "\\data\\ui\\units"):
                if str(dir) != 'merc':
                    try:
                        faction_dir = os.listdir(modpath + "\\data\\ui\\units\\" + str(dir))
                    except:
                        continue
                    unit_cards[str(dir)] = []
                    for unit_card in faction_dir:
                        try:
                            unit_cards[str(dir)].append(unit_card.split('.tga')[0].lower().split('#')[1].lower().strip())
                        except:
                            try:
                                unit_cards[str(dir)].append(unit_card.split('.tga')[0].lower().split('#')[0].lower().strip())
                            except:
                                continue
                if str(dir) == 'mercs':
                    try:
                        faction_dir = os.listdir(modpath + "\\data\\ui\\units\\" + 'mercs')
                    except:
                        continue
                    unit_cards['merc'] = []
                    for unit_card in faction_dir:
                        try:
                            unit_cards['merc'].append(unit_card.split('.tga')[0].lower().split('#')[1].lower().strip())
                        except:
                            try:
                                unit_cards['merc'].append(unit_card.split('.tga')[0].lower().split('#')[0].lower().strip())
                            except:
                                continue
            info_cards = {}
            for dir in os.listdir(modpath + "\\data\\ui\\unit_info"):
                try:
                    faction_dir = os.listdir(modpath + "\\data\\ui\\unit_info\\" + str(dir))
                except:
                    continue
                info_cards[str(dir)] = []
                for info_card in faction_dir:
                    try:
                        info_cards[str(dir)].append(info_card.split('.tga')[0].lower().split('#')[1].lower().split('_info')[0].lower().strip())
                    except:
                        try:
                            info_cards[str(dir)].append(info_card.split('.tga')[0].lower().split('#')[0].lower().split('_info')[0].lower().strip())
                        except:
                            continue

            file_edu.seek(0)
            eduline = 0
            set_card = 0
            set_info = 0
            for line in file_edu:
                eduline += 1
                if re.search(r'^;', line) is not None:
                    continue
                if re.search(r';', line) is not None:
                    line = line.split(';')[0]
                if re.search(r'^type\s', line) is not None:
                    if unit_found == 1 and values['enableownership'] == True:
                        for own_faction in own_factions:
                            try: 
                                if own_faction !=  "":
                                    CheckSilverSurfer(edu_unit.strip(), own_faction.strip(), 'export_descr_unit Ownership', eduline, 'unit', 'faction', set_card, set_info)
                            except:
                                print('something went wrong with ' + edu_unit + " " + own_faction + ' export_descr_unit, line ' + str(eduline) + ' maybe this faction is never mentioned in the bmdb?')
                                continue
                            unit_found = 0
                    edu_unit = re.findall(r'^type\s+(\S.+)', line)[0].strip()
                    upgmodellist = []
                    unit_found = 1
                    officer_dict[edu_unit] = []
                    upgmodel_dict[edu_unit] = []
                    unitmount_dict[edu_unit] = []
                    own_factions = []
                    merc_dict[edu_unit] = 0
                elif re.search(r'^dictionary\s', line) is not None:
                    edu_dicname = re.findall(r'dictionary\s+(\S.+)', line)[0].strip()
                    dicname_dict[edu_unit] = edu_dicname
                elif re.search(r'^category\s', line) is not None:
                    unit_category = re.findall(r'category\s+(\S+)\s', line)[0].strip()
                    unit_ctgdict[edu_unit] = unit_category
                elif re.search(r'^officer\s', line) is not None:
                    if re.findall(r'^officer\s+(\S.+)', line)[0].strip() not in officer_dict[edu_unit]:
                        officer_dict[edu_unit].append(re.findall(r'^officer\s+(\S.+)', line)[0].strip().lower())
                elif re.search(r'^mount\s', line) is not None:
                    mount = re.findall(r'^mount\s+(\S.+)', line)[0].strip()
                    unitmount_dict[edu_unit] = mount
                elif re.search(r'^attributes\s', line) is not None: 
                    if re.search(r'mercenary_unit', line) is not None:
                        merc_dict[edu_unit] = 1
                    else:
                        merc_dict[edu_unit] = 0
                elif re.search(r'^armour_ug_models\s', line) is not None:
                    upgmodels = re.split('\r|,|:|\s', re.findall(r'armour_ug_models\s*(\S.*)', line)[0])
                    for upgmodel in upgmodels:
                        if upgmodel.strip() not in upgmodel_dict[edu_unit] and upgmodel != "":
                            upgmodel_dict[edu_unit].append(upgmodel.strip().lower())
                elif re.search(r'^ownership\s', line) is not None:
                    own_factions = re.split('\r|,|:|\s', re.findall(r'ownership\s*(\S.*)', line)[0])
                elif re.search (r'^info_pic_dir\s', line) is not None and merc_dict[edu_unit] == 0:
                    set_info = 1
                    set_info_faction = re.findall(r'info_pic_dir\s+(\S.+)', line)[0].strip()
                    if dicname_dict[edu_unit].lower().strip() not in info_cards[set_info_faction]:
                        entrycheck = edu_unit+set_info_faction+"info"
                        if entrycheck not in nocardlist:
                            outputfile.write("Unit: " + edu_unit + " " + dicname_dict[edu_unit].lower().strip() + " " + " #Faction: " + set_info_faction + " ### No unit info card as set in edu info_pic_dir!" + "\n" )
                            nocardlist.append(entrycheck)
                elif re.search (r'^card_pic_dir\s', line) is not None and merc_dict[edu_unit] == 0:
                    set_card = 1
                    set_card_faction = re.findall(r'card_pic_dir\s+(\S.+)', line)[0].strip()
                    if set_card_faction == 'mercs':
                        set_card_faction = 'merc'
                    if dicname_dict[edu_unit].lower().strip() not in unit_cards[set_card_faction]:
                        entrycheck = edu_unit+set_card_faction
                        if entrycheck not in nocardlist:
                            outputfile.write("Unit: " + edu_unit + " " + dicname_dict[edu_unit].lower().strip() + " " + " #Faction: " + set_card_faction + " ### No unit card as set in edu card_pic_dir!" + "\n" )
                            nocardlist.append(entrycheck)
            else:
                if unit_found == 1 and values['enableownership'] == True:
                    for own_faction in own_factions:
                        try: 
                            if own_faction !=  "":
                                CheckSilverSurfer(edu_unit.strip(), own_faction.strip(), 'export_descr_unit Ownership', eduline, 'unit', 'faction', set_card, set_info)
                        except:
                            print('something went wrong with ' + edu_unit + " " + own_faction + ' export_descr_unit, line ' + str(eduline) + ' maybe this faction is never mentioned in the bmdb?')
                            continue
                        unit_found = 0

            rp_faction_list = []
            edbline = 0
            file_edb.seek(0)
            for line in file_edb:
                edbline += 1
                if re.search(r'^;', line) is not None:
                    continue
                if re.search(r';', line) is not None:
                    line = line.split(';')[0]
                if re.search(r'recruit_pool', line) is not None:
                    unit = re.findall(r'recruit_pool\s*\"(\S.+)\"', line)[0]
                    try:
                        factions = re.findall(r'recruit_pool\s.*\{(.+)\}', line)[0].split(',')
                    except:
                        factions = ['all']
                    for faction in factions:
                        if faction.strip() != "" and faction.strip() in globalfactionlist:
                            CheckSilverSurfer(unit.strip(), faction.strip(), 'export_descr_buildings', edbline, 'unit', 'faction', '0', '0')
                        elif faction.strip() != "" and faction.strip() in culturelist:
                            CheckSilverSurfer(unit.strip(), faction.strip(), 'export_descr_buildings', edbline, 'unit', 'culture', '0', '0')
            
            file_merc.seek(0)
            mercline = 0
            for line in file_merc:
                mercline += 1
                if re.search(r'^;', line) is not None:
                    continue
                if re.search(r';', line) is not None:
                    line = line.split(';')[0]
                if re.search(r'unit', line) is not None:
                    mercunit = re.split(r'\r|,|:', re.findall(r'unit\s+(.+\S)\s+exp', line)[0])[0]
                    if re.search(r'religions', line) is not None:
                        religions = re.split(r'\r|,|:|\s', re.findall(r'religions \{(.+)\}', line)[0].strip())
                    else:
                        religions = ['all']
                    for religion in religions:
                        if religion.strip() != "" and religion.strip() in religionlist:
                            CheckSilverSurfer(mercunit.strip(), religion.strip(), 'descr_mercenaries', mercline, 'unit', 'religion', '0', '0')

            file_rebels.seek(0)
            rebelsline = 0
            for line in file_rebels:
                rebelsline += 1
                if re.search(r'^;', line) is not None:
                    continue
                if re.search(r';', line) is not None:
                    line = line.split(';')[0]
                if re.search(r'unit', line) is not None:  
                    rebels_unit = re.findall(r'unit\s+(.+\S)', line)[0]
                    CheckSilverSurfer(rebels_unit.strip(), 'slave', 'descr_rebel_factions', rebelsline, 'unit', 'faction', '0', '0')

            linecs = 0
            searchunit = 0
            has_battle_model = 0
            generalunit = 0
            file_cs.seek(0)
            for line in file_cs:
                linecs += 1
                if re.search(r'^;', line) is not None:
                    continue
                if re.search(r';', line) is not None:
                    line = line.split(';')[0]
                if re.search(r'character.*?\s+', line) is not None:
                    has_battle_model = 0
                    if re.search(r'battle_model\s', line) is not None:
                        general_model = re.findall(r'battle_model\s+([:0-z:]+)', line)[0]
                        has_battle_model = 1
                if re.search(r'spawn_army', line) is not None:
                    searchunit = 1
                    generalunit = 1
                if re.search(r'\send\s', line) is not None:
                    searchunit = 0
                if re.search(r'\sfaction\s(.+)\s', line) is not None and searchunit == 1 and re.search(r'sub_faction', line) is None:
                    faction_cs = re.findall(r'\sfaction\s(.+)\s', line)[0]
                if re.search(r'\sfaction\s(.+),', line) is not None and searchunit == 1 and re.search(r'sub_faction', line) is not None:
                    faction_cs = re.findall(r'\sfaction\s(.+),', line)[0]
                if re.search(r'\sunit\s(.+)\s', line) is not None and searchunit == 1:
                    if re.search(r'soldiers', line) is None:
                        cs_unit = re.findall(r'\sunit\s*(.+?)\s*exp', line)[0]
                    else:
                        cs_unit = re.findall(r'\sunit\s*(.+?)\s*soldiers', line)[0]
                    if generalunit == 1 and has_battle_model == 1:
                        CheckSilverSurfer(cs_unit.strip(), faction_cs.strip(), 'campaign_script', linecs, general_model.strip().lower(), 'faction', '0', '0')
                    CheckSilverSurfer(cs_unit.strip(), faction_cs.strip(), 'campaign_script', linecs, 'unit', 'faction', '0', '0')
                    generalunit = 0
                    

            lineds = 0
            has_battle_model = 0
            file_ds.seek(0)
            for line in file_ds:
                lineds += 1
                if re.search(r'^;', line) is not None:
                    continue
                if re.search(r';', line) is not None:
                    line = line.split(';')[0]
                if re.search(r'^faction\s(.+),', line) is not None:
                    faction_ds = re.findall(r'^faction\s(.+),', line)[0]
                if re.search(r'^character.*?\s+', line) is not None:
                    has_battle_model = 0
                    if re.search(r'battle_model\s', line) is not None:
                        general_model = re.findall(r'battle_model\s+([:0-z:]+)', line)[0]
                        has_battle_model = 1
                    searchunit = 0
                if re.search(r'army\s*\n', line) is not None:
                    searchunit = 1
                    generalunit = 1
                if re.search(r'^unit\t+(.+?)\t', line) is not None and searchunit == 1:
                    ds_unit = re.findall(r'^unit\t+(.+?)\t', line)[0]
                    if generalunit == 1 and has_battle_model == 1:
                        CheckSilverSurfer(ds_unit.strip(), faction_ds.strip(), 'descr_strat', lineds, general_model.strip().lower(), 'faction', '0', '0')
                    CheckSilverSurfer(ds_unit.strip(), faction_ds.strip(), 'descr_strat', lineds, 'unit', 'faction', '0', '0')
                    generalunit = 0
            outputfile.flush()
            outputfile.close()
            file_edu.close()
            mounts.close()
            file_cs.close()
            file_ds.close()
            file_bmdb.close()
            file_edb.close()
            file_merc.close()
            file_rebels.close()
            file_smfactions.close()
        #break

        
except Exception as e:
    tb = traceback.format_exc()
    sg.Print(f'An error happened.  Here is the info:', e, tb)
    sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)









    


