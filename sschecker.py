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
sslist = []

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
                            [sg.Button('Check mod', border_width=(3), button_color='#455642', tooltip="Press after selecting a folder or typing a path to confirm, select the modfolder of the mod you want to use"), sg.Button('Quit', border_width=(3), button_color='#780000')]
]

window = sg.Window('Medieval 2 Silver Surfer Checker', layout, finalize=True, resizable=True)

def CheckSilverSurfer(unit, faction, file, line, modeltype, factype):
    if faction != 'scripts':
        if modeltype == 'unit':
            if unit_ctgdict[unit] != 'ship':
                if len(officer_dict[unit]) > 0:
                    for officer in officer_dict[unit]:
                        if factype == 'culture':
                            for cfaction in culturedict[faction]:
                                if merc_dict[unit] == 0:
                                    if officer not in factiondict[cfaction]:
                                        entrycheck = unit+cfaction+officer
                                        if entrycheck not in sslist:
                                            outputfile.write("Unit: " + unit  + " " + " #Faction: " + cfaction + " "+ " #Model: "  + officer + " #On Line "  + str(line) + " in "  + file + " ### Officer model" + "\n")
                                            sslist.append(entrycheck)
                                elif merc_dict[unit] == 1:
                                    if officer not in factiondict['merc']:
                                        entrycheck = unit+"merc"+officer
                                        if entrycheck not in sslist:
                                            outputfile.write("Unit: " + unit  + " " + "#mercenary_unit attribute! " + " #Model: "  + officer + " #On Line "  + str(line) + " in "  + file + " ### Officer model" + "\n")
                                            sslist.append(entrycheck)
                        elif factype == 'faction':
                            if merc_dict[unit] == 0:
                                if officer not in factiondict[faction]:
                                    entrycheck = unit+faction+officer
                                    if entrycheck not in sslist:
                                        outputfile.write("Unit: " + unit  + " " + " #Faction: " + faction + " "+ " #Model: "  + officer + " #On Line "  + str(line) + " in "  + file + " ### Officer model" + "\n")
                                        sslist.append(entrycheck)
                            elif merc_dict[unit] == 1:
                                if officer not in factiondict['merc']:
                                    entrycheck = unit+"merc"+officer
                                    if entrycheck not in sslist:
                                        outputfile.write("Unit: " + unit  + " " + "#mercenary_unit attribute! " + " #Model: "  + officer + " #On Line "  + str(line) + " in "  + file + " ### Officer model" + "\n")
                                        sslist.append(entrycheck)
                for model in upgmodel_dict[unit]:
                    if factype == 'culture':
                        for cfaction in culturedict[faction]:
                            if merc_dict[unit] == 0:
                                if model not in factiondict[cfaction]:
                                    entrycheck = unit+cfaction+model
                                    if entrycheck not in sslist:
                                        outputfile.write("Unit: " + unit  + " " + " #Faction: " + cfaction + " "+ " #Model: "  + model + " #On Line "  + str(line) + " in "  + file + "\n") 
                                        sslist.append(entrycheck)
                            elif merc_dict[unit] == 1:
                                if model not in factiondict['merc']:
                                    entrycheck = unit+"merc"+model
                                    if entrycheck not in sslist:
                                        outputfile.write("Unit: " + unit  + " " + "#mercenary_unit attribute! " + " #Model: "  + model + " #On Line "  + str(line) + " in "  + file + "\n")
                                        sslist.append(entrycheck)
                    elif factype == 'faction':
                        if merc_dict[unit] == 0:
                            if model not in factiondict[faction]:
                                entrycheck = unit+faction+model
                                if entrycheck not in sslist:
                                    outputfile.write("Unit: " + unit  + " " + " #Faction: " + faction + " "+ " #Model: "  + model + " #On Line "  + str(line) + " in "  + file + "\n") 
                                    sslist.append(entrycheck)
                        elif merc_dict[unit] == 1:
                            if model not in factiondict['merc']:
                                entrycheck = unit+"merc"+model
                                if entrycheck not in sslist:
                                    outputfile.write("Unit: " + unit  + " " + "#mercenary_unit attribute! " + " #Model: "  + model + " #On Line "  + str(line) + " in "  + file + "\n")
                                    sslist.append(entrycheck)
            try:
                mountmodel = mountdict[unitmount_dict[unit]]
                if factype == 'culture':
                    for cfaction in culturedict[faction]:
                        if merc_dict[unit] == 0:
                            if mountmodel not in factiondict[cfaction]:
                                entrycheck = unit+cfaction+mountmodel
                                if entrycheck not in sslist:
                                    outputfile.write("Unit: " + unit  + " " + " #Faction: " + cfaction + " "+ " #Model: "  + mountmodel + " #On Line "  + str(line) + " in "  + file + " ### Mount" + "\n")  
                                    sslist.append(entrycheck)
                        elif merc_dict[unit] == 1:
                            if mountmodel not in factiondict['merc']:
                                entrycheck = unit+"merc"+mountmodel
                                if entrycheck not in sslist:
                                    outputfile.write("Unit: " + unit  + " " + "#mercenary_unit attribute! " + " #Model: "  + mountmodel + " #On Line "  + str(line) + " in "  + file + " ### Mount" + "\n")
                                    sslist.append(entrycheck)
                if factype == 'faction':
                    if merc_dict[unit] == 0:
                        if mountmodel not in factiondict[faction]:
                            entrycheck = unit+faction+mountmodel
                            if entrycheck not in sslist:
                                outputfile.write("Unit: " + unit  + " " + " #Faction: " + faction + " "+ " #Model: "  + mountmodel + " #On Line "  + str(line) + " in "  + file + " ### Mount" + "\n")  
                                sslist.append(entrycheck)
                    elif merc_dict[unit] == 1:
                        if mountmodel not in factiondict['merc']:
                            entrycheck = unit+"merc"+mountmodel
                            if entrycheck not in sslist:
                                outputfile.write("Unit: " + unit  + " " + "#mercenary_unit attribute! " + " #Model: "  + mountmodel + " #On Line "  + str(line) + " in "  + file + " ### Mount" + "\n")
                                sslist.append(entrycheck)
            except:
                    mountmodel = ""           
        if modeltype != 'unit':
            if merc_dict[unit] == 0:
                if modeltype not in factiondict[faction]:
                    entrycheck = unit+faction+modeltype
                    if entrycheck not in sslist:
                        outputfile.write("Unit: " + unit  + " " + " #Faction: " + faction + " "+ " #Model: "  + modeltype + " #On Line "  + str(line) + " in "  + file + " ### General" + "\n")
                        sslist.append(entrycheck)
            if merc_dict[unit] == 1:
                if modeltype not in factiondict['merc']:
                    entrycheck = unit+"merc"+modeltype
                    if entrycheck not in sslist:
                        outputfile.write("Unit: " + unit  + " " + "#mercenary_unit attribute! " + " #Model: "  + modeltype + " #On Line "  + str(line) + " in "  + file + " ### General" + "\n")
                        sslist.append(entrycheck)

try:
    while True: 
        event, values = window.read()
        
        # -------------------------Quit button-------------------------------------------
        if event == sg.WIN_CLOSED or event == 'Quit':
            break
        
        if event == 'Check mod':
            if (values['modpath']) != "":
                modpath = values['modpath']
            eduname = modpath + "\\data\\export_descr_unit.txt"
            edbname = modpath + "\\data\\export_descr_buildings.txt"
            bmdbname = modpath + "\\data\\unit_models\\battle_models.modeldb"
            mountsname = modpath + "\\data\\descr_mount.txt"
            smfactionsname = modpath + "\\data\\descr_sm_factions.txt"
            outputfilename = modpath + "\\silver_surfers.txt"
            dsname = modpath + "\\data\\world\\maps\\campaign\\imperial_campaign\\descr_strat.txt"
            csname = modpath + "\\data\\world\\maps\\campaign\\imperial_campaign\\campaign_script.txt"

            encodings = ['utf8', 'cp1252', 'cp1250']

            for i in encodings:
                try:
                    file_edu = open(eduname, 'r', encoding=i)
                    file_edu.readlines()
                    file_edu.seek(0)
                    break
                except UnicodeDecodeError:
                    continue

            for i in encodings:
                    try:
                        mounts = open(mountsname, encoding=i)
                        mounts.readlines()
                        mounts.seek(0)
                        break
                    except UnicodeDecodeError:
                        continue

            for i in encodings:
                try:
                    file_cs = open(csname, encoding=i)
                    file_cs.readlines()
                    file_cs.seek(0)
                    break
                except UnicodeDecodeError:
                    continue 

            for i in encodings:
                try:
                    file_ds = open(dsname, encoding=i)
                    file_ds.readlines()
                    file_ds.seek(0)
                    break
                except UnicodeDecodeError:
                    continue   

            outputfile = open(outputfilename, 'w') 
            file_bmdb = open(bmdbname, 'r', encoding='utf8')
            file_edb = open(edbname, 'r', encoding='utf8')
            file_smfactions = open(smfactionsname, 'r', encoding='utf8')

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

            for line in file_edu:
                if re.search(r'^;', line) is not None:
                    continue
                if re.search(r';', line) is not None:
                    line = line.split(';')[0]
                if re.search(r'^type\s', line) is not None:
                    edu_unit = re.findall(r'^type\s+(\S.+)', line)[0].strip()
                    upgmodellist = []
                    unit_found = 1
                    officer_dict[edu_unit] = []
                    upgmodel_dict[edu_unit] = []
                    unitmount_dict[edu_unit] = []
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
                    upgregex = re.findall(r'armour_ug_models\s*(\S.*)', line)[0]
                    upgmodels = upgregex.split(',')
                    for upgmodel in upgmodels:
                        if upgmodel.strip() not in upgmodel_dict[edu_unit]:
                            upgmodel_dict[edu_unit].append(upgmodel.strip().lower())

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

            rp_faction_list = []
            edbline = 0
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
                            CheckSilverSurfer(unit.strip(), faction.strip(), 'export_descr_buildings', edbline, 'unit', 'faction')
                        elif faction.strip() != "" and faction.strip() in culturelist:
                            CheckSilverSurfer(unit.strip(), faction.strip(), 'export_descr_buildings', edbline, 'unit', 'culture')
                        
            linecs = 0
            searchunit = 0
            has_battle_model = 0
            generalunit = 0
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
                        CheckSilverSurfer(cs_unit.strip(), faction_cs.strip(), 'campaign_script', linecs, general_model.strip().lower(), 'faction')
                    CheckSilverSurfer(cs_unit.strip(), faction_cs.strip(), 'campaign_script', linecs, 'unit', 'faction')
                    generalunit = 0
                    

            lineds = 0
            has_battle_model = 0
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
                        CheckSilverSurfer(ds_unit.strip(), faction_ds.strip(), 'descr_strat', lineds, general_model.strip().lower(), 'faction')
                    CheckSilverSurfer(ds_unit.strip(), faction_ds.strip(), 'descr_strat', lineds, 'unit', 'faction')
                    generalunit = 0
        outputfile.flush()
        outputfile.close()
        
except Exception as e:
    tb = traceback.format_exc()
    sg.Print(f'An error happened.  Here is the info:', e, tb)
    sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)







    


