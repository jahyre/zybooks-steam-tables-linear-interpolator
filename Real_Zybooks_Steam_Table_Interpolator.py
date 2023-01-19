########################################################################################################################
# zybooks steam table interpolator
########################################################################################################################

import pandas as pd
import interlib as lb

file_path1 = "C:/Users/jacks/Desktop/School/CBEE/Zybooks steam table saturated water t.xlsx"
file_path2 = "C:/Users/jacks/Desktop/School/CBEE/zybooks_superheated_vapor_steam_table.xlsx"
file_path3 = "C:/Users/jacks/Desktop/School/CBEE/zybooks_subcooled_liquid_steam_table.xlsx"
sat = pd.read_excel(file_path1)


#  isolating columns
tsat_list = list(sat.loc[:, 'T, °C'])
psat_list = list(sat.loc[:, 'Psat, kPa'])
vfsat_list = list(sat.loc[:, 'vf'])
vgsat_list = list(sat.loc[:, 'vg'])
ufsat_list = list(sat.loc[:, 'uf'])
ugsat_list = list(sat.loc[:, 'ug'])
ufgsat_list = list(sat.loc[:, 'ufg'])
hfsat_list = list(sat.loc[:, 'hf'])
hgsat_list = list(sat.loc[:, 'hg'])
hfgsat_list = list(sat.loc[:, 'hfg'])
sfsat_list = list(sat.loc[:, 'sf'])
sgsat_list = list(sat.loc[:, 'sg'])
sfgsat_list = list(sat.loc[:, 'sfg'])


superheated_pressures = [10, 50, 100, 200, 300, 400, 500, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2500, 3000,
                         3500, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 17000,
                         20000]
subcooled_pressures = [10, 50, 100, 250, 500, 1000, 2500, 5000, 7500, 10000, 15000, 20000]

########################################################################################################################
# checking values
########################################################################################################################
while True:
    temp = float(input("starting temperature (°C): ") or 10)
    if float(373.946) >= float(temp) >= 0.01:
        break
    else:
        print('that is not a value that can be interpolated with the zybooks steam tables')
        continue
while True:
    pressure = float(input("starting pressure (kPa): ") or 1000)
    if 22064 >= float(pressure) >= 0.612:
        break
    else:
        print('that is not a value that can be interpolated with the zybooks steam tables')
        continue

########################################################################################################################
# interpolating, checking table
########################################################################################################################

if float(temp) in list(tsat_list):
    for i in range(len(tsat_list)):
        if float(tsat_list[i]) == float(temp):
            psat_expect = float(psat_list[i])


else:
    tsat_below, tsat_above = lb.above_below(float(temp), tsat_list)
    psat_below, psat_above = lb.corresponding_ab(float(temp), tsat_list, psat_list)
    psat_expect = psat_below + ((psat_above - psat_below) / (tsat_above - tsat_below)) * (temp - tsat_below)

if psat_expect - .5 < pressure < .5 + psat_expect:
    for i in range(len(tsat_list)):
        if float(tsat_list[i]) == float(temp):
            vf_sat = float(vfsat_list[i])
            vg_sat = float(vgsat_list[i])
            uf_sat = float(ufsat_list[i])
            ug_sat = float(ugsat_list[i])
            ufg_sat = float(ufgsat_list[i])
            hf_sat = float(hfsat_list[i])
            hg_sat = float(hgsat_list[i])
            hfg_sat = float(hfgsat_list[i])
            sf_sat = float(sfsat_list[i])
            sg_sat = float(sgsat_list[i])
            sfg_sat = float(sfgsat_list[i])
            print("T = "+str(temp)+" °C\nP = "+str(psat_expect)+" kPa\nvf = "+str(vf_sat)+" m^3/kg\nvg = "+str(vg_sat) +
                  "m^3/kg\nuf = "+str(uf_sat)+" kJ/kg\nug = "+str(ug_sat)+" kJ/kg\nufg = "+str(ufg_sat)+" kJ/kg\nhf = "
                  + str(hfg_sat)+" kJ/kg\nsf = "+str(sf_sat)+" K*kJ/kg\nsg = "+str(sg_sat)+" K*kJ/kg\nsfg = " +
                  str(sfg_sat)+" K*kJ/kg")

if pressure < (psat_expect - .5):  # superheated vapor
    if pressure in superheated_pressures:
        for q in range(len(superheated_pressures)):
            if pressure == superheated_pressures[q]:
                superheated = pd.read_excel(file_path2, q)
                theated_list = superheated.loc[:, 'T']
                vheated_list = superheated.loc[:, 'v']
                uheated_list = superheated.loc[:, 'u']
                hheated_list = superheated.loc[:, 'h']
                sheated_list = superheated.loc[:, 's']
        if temp in list(theated_list):
            index = lb.find_index(temp, theated_list)
            v = list(vheated_list)[index]
            u = list(uheated_list)[index]
            h = list(hheated_list)[index]
            s = list(sheated_list)[index]
            print("v = "+str(v)+" m^3/kg\nu = "+str(u)+" kJ/kg\nh = "+str(h)+" kJ/kg\ns = "+str(s)+" K*kJ/kg")
        else:
            temp_b, temp_a = lb.above_below(temp, list(theated_list))
            v_b, v_a = lb.corresponding_ab(temp, theated_list, vheated_list)
            u_b, u_a = lb.corresponding_ab(temp, theated_list, uheated_list)
            h_b, h_a = lb.corresponding_ab(temp, theated_list, hheated_list)
            s_b, s_a = lb.corresponding_ab(temp, theated_list, sheated_list)
            v = lb.interpolate(temp, temp_b, temp_a, v_b, v_a)
            u = lb.interpolate(temp, temp_b, temp_a, u_b, u_a)
            h = lb.interpolate(temp, temp_b, temp_a, h_b, h_a)
            s = lb.interpolate(temp, temp_b, temp_a, s_b, s_a)
            print("v = "+str(v)+" m^3/kg\nu = "+str(u)+" kJ/kg\nh = "+str(h)+" kJ/kg\ns = "+str(s)+" K*kJ/kg")

    elif pressure not in superheated_pressures:
        pressure_below, pressure_above = lb.above_below(pressure, superheated_pressures)
        for l in range(len(superheated_pressures)):
             if pressure_below == superheated_pressures[l]:
                 superheatedb = pd.read_excel(file_path2, l)
                 theatedb_list = superheatedb.loc[:, 'T']
                 vheatedb_list = superheatedb.loc[:, 'v']
                 uheatedb_list = superheatedb.loc[:, 'u']
                 hheatedb_list = superheatedb.loc[:, 'h']
                 sheatedb_list = superheatedb.loc[:, 's']
             elif pressure_above == superheated_pressures[l]:
                 superheateda = pd.read_excel(file_path2, l)
                 theateda_list = superheateda.loc[:, 'T']
                 vheateda_list = superheateda.loc[:, 'v']
                 uheateda_list = superheateda.loc[:, 'u']
                 hheateda_list = superheateda.loc[:, 'h']
                 sheateda_list = superheateda.loc[:, 's']
        theated_list = lb.interpolist(pressure, pressure_below, pressure_above, list(theatedb_list),
                                      list(theateda_list))
        vheated_list = lb.interpolist(pressure, pressure_below, pressure_above, list(vheatedb_list),
                                      list(vheateda_list))
        uheated_list = lb.interpolist(pressure, pressure_below, pressure_above, list(uheatedb_list),
                                      list(uheateda_list))
        hheated_list = lb.interpolist(pressure, pressure_below, pressure_above, list(hheatedb_list),
                                      list(hheateda_list))
        sheated_list = lb.interpolist(pressure, pressure_below, pressure_above, list(sheatedb_list),
                                      list(sheateda_list))
        temp_b, temp_a = lb.above_below(temp, list(theated_list))
        v_b, v_a = lb.corresponding_ab(temp, theated_list, vheated_list)
        u_b, u_a = lb.corresponding_ab(temp, theated_list, uheated_list)
        h_b, h_a = lb.corresponding_ab(temp, theated_list, hheated_list)
        s_b, s_a = lb.corresponding_ab(temp, theated_list, sheated_list)
        v = lb.interpolate(temp, temp_b, temp_a, v_b, v_a)
        u = lb.interpolate(temp, temp_b, temp_a, u_b, u_a)
        h = lb.interpolate(temp, temp_b, temp_a, h_b, h_a)
        s = lb.interpolate(temp, temp_b, temp_a, s_b, s_a)
        print("v = "+str(v)+" m^3/kg\nu = "+str(u)+" kJ/kg\nh = "+str(h)+" kJ/kg\ns = "+str(s)+" K*kJ/kg")

elif pressure > psat_expect + .5:  # subcooled liquid
    if pressure in subcooled_pressures:
        for q in range(len(subcooled_pressures)):
            if pressure == subcooled_pressures[q]:
                subcooled = pd.read_excel(file_path3, q)
                tcooled_list = subcooled.loc[:, 'T']
                vcooled_list = subcooled.loc[:, 'v']
                ucooled_list = subcooled.loc[:, 'u']
                hcooled_list = subcooled.loc[:, 'h']
                scooled_list = subcooled.loc[:, 's']
        if temp in list(tcooled_list):
            index = lb.find_index(temp, tcooled_list)
            v = list(vcooled_list)[index]
            u = list(ucooled_list)[index]
            h = list(hcooled_list)[index]
            s = list(scooled_list)[index]
            print("v = "+str(v)+" m^3/kg\nu = "+str(u)+" kJ/kg\nh = "+str(h)+" kJ/kg\ns = "+str(s)+" K*kJ/kg")
        else:
            temp_b, temp_a = lb.above_below(temp, list(tcooled_list))
            v_b, v_a = lb.corresponding_ab(temp, tcooled_list, vcooled_list)
            u_b, u_a = lb.corresponding_ab(temp, tcooled_list, ucooled_list)
            h_b, h_a = lb.corresponding_ab(temp, tcooled_list, hcooled_list)
            s_b, s_a = lb.corresponding_ab(temp, tcooled_list, scooled_list)
            v = lb.interpolate(temp, temp_b, temp_a, v_b, v_a)
            u = lb.interpolate(temp, temp_b, temp_a, u_b, u_a)
            h = lb.interpolate(temp, temp_b, temp_a, h_b, h_a)
            s = lb.interpolate(temp, temp_b, temp_a, s_b, s_a)
            print("v = "+str(v)+" m^3/kg\nu = "+str(u)+" kJ/kg\nh = "+str(h)+" kJ/kg\ns = "+str(s)+" K*kJ/kg")
    elif pressure not in subcooled_pressures:
        pressure_below, pressure_above = lb.above_below(pressure, subcooled_pressures)
        for l in range(len(subcooled_pressures)):
             if pressure_below == subcooled_pressures[l]:
                 subcooledb = pd.read_excel(file_path3, l)
                 tcooledb_list = subcooledb.loc[:, 'T']
                 vcooledb_list = subcooledb.loc[:, 'v']
                 ucooledb_list = subcooledb.loc[:, 'u']
                 hcooledb_list = subcooledb.loc[:, 'h']
                 scooledb_list = subcooledb.loc[:, 's']
             elif pressure_above == subcooled_pressures[l]:
                 subcooleda = pd.read_excel(file_path3, l)
                 tcooleda_list = list(subcooleda.loc[:, 'T'])
                 vcooleda_list = list(subcooleda.loc[:, 'v'])
                 ucooleda_list = list(subcooleda.loc[:, 'u'])
                 hcooleda_list = list(subcooleda.loc[:, 'h'])
                 scooleda_list = list(subcooleda.loc[:, 's'])
        tcooled_list = lb.interpolist(pressure, pressure_below, pressure_above, list(tcooledb_list),
                                      list(tcooleda_list))
        vcooled_list = lb.interpolist(pressure, pressure_below, pressure_above, list(vcooledb_list),
                                      list(vcooleda_list))
        ucooled_list = lb.interpolist(pressure, pressure_below, pressure_above, list(ucooledb_list),
                                      list(ucooleda_list))
        hcooled_list = lb.interpolist(pressure, pressure_below, pressure_above, list(hcooledb_list),
                                      list(hcooleda_list))
        scooled_list = lb.interpolist(pressure, pressure_below, pressure_above, list(scooledb_list),
                                      list(scooleda_list))
        temp_b, temp_a = lb.above_below(temp, list(tcooled_list))
        v_b, v_a = lb.corresponding_ab(temp, tcooled_list, vcooled_list)
        u_b, u_a = lb.corresponding_ab(temp, tcooled_list, ucooled_list)
        h_b, h_a = lb.corresponding_ab(temp, tcooled_list, hcooled_list)
        s_b, s_a = lb.corresponding_ab(temp, tcooled_list, scooled_list)
        v = lb.interpolate(temp, temp_b, temp_a, v_b, v_a)
        u = lb.interpolate(temp, temp_b, temp_a, u_b, u_a)
        h = lb.interpolate(temp, temp_b, temp_a, h_b, h_a)
        s = lb.interpolate(temp, temp_b, temp_a, s_b, s_a)
        print("v = "+str(v)+" m^3/kg\nu = "+str(u)+" kJ/kg\nh = "+str(h)+" kJ/kg\ns = "+str(s)+" K*kJ/kg")
