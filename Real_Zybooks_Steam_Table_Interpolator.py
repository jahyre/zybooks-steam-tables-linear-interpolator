########################################################################################################################
# zybooks steam table interpolator
########################################################################################################################

import pandas as pd
import interlib as lb

file_path1 = "C:/Users/jacks/Desktop/School/Zybooks Linear Interpolator/Zybooks steam table saturated water t.xlsx"
file_path2 = "C:/Users/jacks/Desktop/School/Zybooks Linear Interpolator/zybooks_superheated_vapor_steam_table.xlsx"
file_path3 = "C:/Users/jacks/Desktop/School/Zybooks Linear Interpolator/zybooks_subcooled_liquid_steam_table.xlsx"
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

m1 = float(input("What is the inlet flow rate in kg/s? "))

########################################################################################################################
# interpolating, checking table
########################################################################################################################

if float(temp) in list(tsat_list):
    for i in range(len(tsat_list)):
        if float(tsat_list[i]) == float(temp):
            psat_expect = float(psat_list[i])
    print(str(psat_expect))
else:
    tsat_below, tsat_above = lb.above_below(float(temp), tsat_list)
    psat_below, psat_above = lb.corresponding_ab(float(temp), tsat_list, psat_list)
    psat_expect = psat_below + ((psat_above - psat_below) / (tsat_above - tsat_below)) * (temp - tsat_below)
    print(str(psat_expect))

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
            print("Saturated\nT = " + str(temp) + " °C\nP = " + str(psat_expect) + " kPa\nvf = " + str(
                vf_sat) + " m^3/kg\nvg = " + str(vg_sat) +
                  "m^3/kg\nuf = " + str(uf_sat) + " kJ/kg\nug = " + str(ug_sat) + " kJ/kg\nufg = " + str(
                ufg_sat) + " kJ/kg\nhf = "
                  + str(hfg_sat) + " kJ/kg\nsf = " + str(sf_sat) + " K*kJ/kg\nsg = " + str(
                sg_sat) + " K*kJ/kg\nsfg = " +
                  str(sfg_sat) + " K*kJ/kg")

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
            v1 = list(vheated_list)[index]
            u1 = list(uheated_list)[index]
            h1 = list(hheated_list)[index]
            s1 = list(sheated_list)[index]
            print("Super Heated Vapor\nv = " + str(v1) + " m^3/kg\nu = " + str(u1) + " kJ/kg\nh = " + str(
                h1) + " kJ/kg\ns = " + str(s1) + " K*kJ/kg")
        else:
            temp_b, temp_a = lb.above_below(temp, list(theated_list))
            v_b, v_a = lb.corresponding_ab(temp, theated_list, vheated_list)
            u_b, u_a = lb.corresponding_ab(temp, theated_list, uheated_list)
            h_b, h_a = lb.corresponding_ab(temp, theated_list, hheated_list)
            s_b, s_a = lb.corresponding_ab(temp, theated_list, sheated_list)
            v1 = lb.interpolate(temp, temp_b, temp_a, v_b, v_a)
            u1 = lb.interpolate(temp, temp_b, temp_a, u_b, u_a)
            h1 = lb.interpolate(temp, temp_b, temp_a, h_b, h_a)
            s1 = lb.interpolate(temp, temp_b, temp_a, s_b, s_a)
            print("Superheated Vapor\nv = " + str(v1) + " m^3/kg\nu = " + str(u1) + " kJ/kg\nh = " + str(
                h1) + " kJ/kg\ns = " + str(s1) + " K*kJ/kg")

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
        v1 = lb.interpolate(temp, temp_b, temp_a, v_b, v_a)
        u1 = lb.interpolate(temp, temp_b, temp_a, u_b, u_a)
        h1 = lb.interpolate(temp, temp_b, temp_a, h_b, h_a)
        s1 = lb.interpolate(temp, temp_b, temp_a, s_b, s_a)
        print("Superheated Vapor\nv = " + str(v1) + " m^3/kg\nu = " + str(u1) + " kJ/kg\nh = " + str(
            h1) + " kJ/kg\ns = " + str(s1) + " K*kJ/kg")

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
            v1 = list(vcooled_list)[index]
            u1 = list(ucooled_list)[index]
            h1 = list(hcooled_list)[index]
            s1 = list(scooled_list)[index]
            print("Subcooled Liquid\nv = " + str(v1) + " m^3/kg\nu = " + str(u1) + " kJ/kg\nh = " + str(
                h1) + " kJ/kg\ns = " + str(s1) + " K*kJ/kg")
        else:
            temp_b, temp_a = lb.above_below(temp, list(tcooled_list))
            v_b, v_a = lb.corresponding_ab(temp, tcooled_list, vcooled_list)
            u_b, u_a = lb.corresponding_ab(temp, tcooled_list, ucooled_list)
            h_b, h_a = lb.corresponding_ab(temp, tcooled_list, hcooled_list)
            s_b, s_a = lb.corresponding_ab(temp, tcooled_list, scooled_list)
            v1 = lb.interpolate(temp, temp_b, temp_a, v_b, v_a)
            u1 = lb.interpolate(temp, temp_b, temp_a, u_b, u_a)
            h1 = lb.interpolate(temp, temp_b, temp_a, h_b, h_a)
            s1 = lb.interpolate(temp, temp_b, temp_a, s_b, s_a)
            print("Subcooled Liquid\nv = " + str(v1) + " m^3/kg\nu = " + str(u1) + " kJ/kg\nh = " + str(
                h1) + " kJ/kg\ns = " + str(s1) + " K*kJ/kg")
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
        v1 = lb.interpolate(temp, temp_b, temp_a, v_b, v_a)
        u1 = lb.interpolate(temp, temp_b, temp_a, u_b, u_a)
        h1 = lb.interpolate(temp, temp_b, temp_a, h_b, h_a)
        s1 = lb.interpolate(temp, temp_b, temp_a, s_b, s_a)
        print("\Subcooled Liquid\nv = " + str(v1) + " m^3/kg\nu = " + str(u1) + " kJ/kg\nh = " + str(
            h1) + " kJ/kg\ns = " + str(s1) + " K*kJ/kg")

# outlet
answer_saturated = str(input("Is your outlet known to be saturated? (y/n) "))
if answer_saturated == str("y"):
    q_or_m = str(input("Are you solving for m2 and m3 or Q? (m/Q) "))
    if q_or_m == str("m"):
        Q = float(input("What is the change in heat in kJ/s? "))
        P2 = float(input("What is your ending pressure in kPa? "))
        for i in range(len(list(psat_list))):
            if P2 in list(psat_list):
                if P2 == (list(psat_list)[i]):
                    T2 = (list(tsat_list)[i])
            else:
                p2_below, p2_above = lb.above_below(P2, list(psat_list))
                t2_below, t2_above = lb.corresponding_ab(P2, list(psat_list), list(tsat_list))
                T2 = lb.interpolate(P2, p2_below, p2_above, t2_below, t2_above)
                hg2_below, hg2_above = lb.corresponding_ab(P2, list(psat_list), list(hgsat_list))
                hg2 = lb.interpolate(P2, p2_below, p2_above, hg2_below, hg2_above)
                hf3_below, hf3_above = lb.corresponding_ab(P2, list(psat_list), list(hfsat_list))
                hf3 = lb.interpolate(P2, p2_below, p2_above, hf3_below, hf3_above)
                m2 = (m1 * (h1 - hf3) + Q) / (hg2 - hf3)
                m3 = m1 - m2
        print("T2 = "+str(T2)+" °C\nMass In Gas Phase = "+str(m2)+" kg/s\nMass In Liquid Phase = "+str(m3) +
              " kg/s\nhf = "+str(hf3)+" kJ/kg\nhg = "+str(hg2)+" kJ/kg")
    elif q_or_m == str("Q"):
        m2 = float(input("What is the outlet mass flow rate in the gas phase in kg/s "))
        m3 = float(input("What is the outlet mass flow rate in the liquid phase in kg/s "))
        P2 = float(input("What is your ending pressure in kPa? "))
        for i in range(len(list(psat_list))):
            if P2 in list(psat_list):
                if P2 == (list(psat_list)[i]):
                    T2 = (list(tsat_list)[i])
            else:
                p2_below, p2_above = lb.above_below(P2, list(psat_list))
                t2_below, t2_above = lb.corresponding_ab(P2, list(psat_list), list(tsat_list))
                T2 = lb.interpolate(P2, p2_below, p2_above, t2_below, t2_above)
                hg2_below, hg2_above = lb.corresponding_ab(P2, list(psat_list), list(hgsat_list))
                hg2 = lb.interpolate(P2, p2_below, p2_above, hg2_below, hg2_above)
                hf3_below, hf3_above = lb.corresponding_ab(P2, list(psat_list), list(hfsat_list))
                hf3 = lb.interpolate(P2, p2_below, p2_above, hf3_below, hf3_above)
                Q = m2 * hg2 + m3 * hf3 - m1 * h1
        print("T2 = " + str(T2) + " °C\nQ = " + str(Q) + " kJ/s\nhf = " + str(hf3) + " kJ/kg\nhg = " + str(
            hg2) + " kJ/kg")

elif answer_saturated == str("n"):
    q_or_t = str(input("Are you solving for T2 or Q? (T2/Q) "))
    if q_or_t == str("T2"):
        Q = float(input("What is the change in heat in kJ/s? "))
        P2 = float(input("What is your ending pressure in kPa? "))
        m2 = float(input("What is your outlet mass flow rate in kg/s? "))
        h2 = (Q - h1 * m1) / m2 * (-1)
        if P2 in list(psat_list):
            for i in range(len(list(psat_list))):
                if P2 == list(psat_list)[i] and h2 < (list(hfsat_list))[i]:
                    # subcooled liquid
                    if P2 in subcooled_pressures:
                        for q in range(len(subcooled_pressures)):
                            if P2 == subcooled_pressures[q]:
                                subcooled2 = pd.read_excel(file_path3, q)
                                tcooled2_list = subcooled2.loc[:, 'T']
                                vcooled2_list = subcooled2.loc[:, 'v']
                                ucooled2_list = subcooled2.loc[:, 'u']
                                hcooled2_list = subcooled2.loc[:, 'h']
                                scooled2_list = subcooled2.loc[:, 's']
                        if h2 in list(hcooled2_list):
                            index = lb.find_index(h2, hcooled2_list)
                            v2 = list(vcooled2_list)[index]
                            u2 = list(ucooled2_list)[index]
                            t2 = list(tcooled_list)[index]
                            s2 = list(scooled2_list)[index]
                            print("Subcooled Liquid\nv2 = " + str(v2) + " m^3/kg\nu2 = " + str(u2) + " kJ/kg\nT2 = " + str(
                                t2) + " C\ns2 = " + str(s2) + " K*kJ/kg")
                        else:
                            h_b2, h_a2 = lb.above_below(h2, list(hcooled2_list))
                            v_b2, v_a2 = lb.corresponding_ab(h2, hcooled2_list, vcooled2_list)
                            u_b2, u_a2 = lb.corresponding_ab(h2, hcooled2_list, ucooled2_list)
                            t_b2, t_a2 = lb.corresponding_ab(h2, hcooled2_list, tcooled2_list)
                            s_b2, s_a2 = lb.corresponding_ab(h2, hcooled2_list, scooled2_list)
                            v2 = lb.interpolate(h2, h_b2, h_a2, v_b2, v_a2)
                            u2 = lb.interpolate(h2, h_b2, h_a2, u_b2, u_a2)
                            t2 = lb.interpolate(h2, h_b2, h_a2, t_b2, t_a2)
                            s2 = lb.interpolate(h2, h_b2, h_a2, s_b2, s_a2)
                            print("Subcooled Liquid\nv2 = " + str(v2) + " m^3/kg\nu2 = " + str(u2) + " kJ/kg\nT2 = " + str(
                                t2) + " C\ns2 = " + str(s2) + " K*kJ/kg")
                    elif P2 not in subcooled_pressures:
                        pressure_below, pressure_above = lb.above_below(pressure, subcooled_pressures)
                        for l in range(len(subcooled_pressures)):
                            if pressure_below == subcooled_pressures[l]:
                                subcooledb2 = pd.read_excel(file_path3, l)
                                tcooledb2_list = list(subcooledb2.loc[:, 'T'])
                                vcooledb2_list = list(subcooledb2.loc[:, 'v'])
                                ucooledb2_list = list(subcooledb2.loc[:, 'u'])
                                hcooledb2_list = list(subcooledb2.loc[:, 'h'])
                                scooledb2_list = list(subcooledb2.loc[:, 's'])
                            elif pressure_above == subcooled_pressures[l]:
                                subcooleda2 = pd.read_excel(file_path3, l)
                                tcooleda2_list = list(subcooleda2.loc[:, 'T'])
                                vcooleda2_list = list(subcooleda2.loc[:, 'v'])
                                ucooleda2_list = list(subcooleda2.loc[:, 'u'])
                                hcooleda2_list = list(subcooleda2.loc[:, 'h'])
                                scooleda2_list = list(subcooleda2.loc[:, 's'])
                        tcooled2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(tcooledb2_list),
                                                      list(tcooleda2_list))
                        vcooled2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(vcooledb2_list),
                                                      list(vcooleda2_list))
                        ucooled2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(ucooledb2_list),
                                                      list(ucooleda2_list))
                        hcooled2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(hcooledb2_list),
                                                      list(hcooleda2_list))
                        scooled2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(scooledb2_list),
                                                      list(scooleda2_list))
                        h_b2, h_a2 = lb.above_below(temp, list(hcooled2_list))
                        v_b2, v_a2 = lb.corresponding_ab(h2, hcooled2_list, vcooled2_list)
                        u_b2, u_a2 = lb.corresponding_ab(h2, hcooled2_list, ucooled2_list)
                        t_b2, t_a2 = lb.corresponding_ab(h2, hcooled2_list, tcooled2_list)
                        s_b2, s_a2 = lb.corresponding_ab(h2, hcooled2_list, scooled2_list)
                        v2 = lb.interpolate(h2, h_b2, h_a2, v_b2, v_a2)
                        u2 = lb.interpolate(h2, h_b2, h_a2, u_b2, u_a2)
                        t2 = lb.interpolate(h2, h_b2, h_a2, t_b2, t_a2)
                        s2 = lb.interpolate(h2, h_b2, h_a2, s_b2, s_a2)
                        print("Subcooled Liquid\nv2 = " + str(v2) + " m^3/kg\nu2 = " + str(u2) + " kJ/kg\nT2 = " + str(
                            t2) + " C\ns2 = " + str(s2) + " K*kJ/kg")
                elif P2 == list(psat_list)[i] and h2 > (list(hgsat_list))[i]:
                    # Superheated Vapor
                    if P2 in superheated_pressures:
                        for q in range(len(superheated_pressures)):
                            if P2 == subcooled_pressures[q]:
                                superheated2 = pd.read_excel(file_path3, q)
                                theated2_list = superheated2.loc[:, 'T']
                                vheated2_list = superheated2.loc[:, 'v']
                                uheated2_list = superheated2.loc[:, 'u']
                                hheated2_list = superheated2.loc[:, 'h']
                                sheated2_list = superheated2.loc[:, 's']
                        if h2 in list(hheated2_list):
                            index = lb.find_index(h2, hheated2_list)
                            v2 = list(vheated2_list)[index]
                            u2 = list(uheated2_list)[index]
                            t2 = list(theated_list)[index]
                            s2 = list(sheated2_list)[index]
                            print("Superheated Vapor\nv2 = " + str(v2) + " m^3/kg\nu2 = " + str(
                                u2) + " kJ/kg\nT2 = " + str(
                                t2) + " C\ns2 = " + str(s2) + " K*kJ/kg")
                        else:
                            h_b2, h_a2 = lb.above_below(h2, list(hheated2_list))
                            v_b2, v_a2 = lb.corresponding_ab(h2, hheated2_list, vheated2_list)
                            u_b2, u_a2 = lb.corresponding_ab(h2, hheated2_list, uheated2_list)
                            t_b2, t_a2 = lb.corresponding_ab(h2, hheated2_list, theated2_list)
                            s_b2, s_a2 = lb.corresponding_ab(h2, hheated2_list, sheated2_list)
                            v2 = lb.interpolate(h2, h_b2, h_a2, v_b2, v_a2)
                            u2 = lb.interpolate(h2, h_b2, h_a2, u_b2, u_a2)
                            t2 = lb.interpolate(h2, h_b2, h_a2, t_b2, t_a2)
                            s2 = lb.interpolate(h2, h_b2, h_a2, s_b2, s_a2)
                            print("Superheated Vapor\nv2 = " + str(v2) + " m^3/kg\nu2 = " + str(
                                u2) + " kJ/kg\nT2 = " + str(
                                t2) + " C\ns2 = " + str(s2) + " K*kJ/kg")
                    elif P2 not in superheated_pressures:
                        pressure_below, pressure_above = lb.above_below(pressure, superheated_pressures)
                        for l in range(len(superheated_pressures)):
                            if pressure_below == superheated_pressures[l]:
                                superheatedb2 = pd.read_excel(file_path3, l)
                                theatedb2_list = list(superheatedb2.loc[:, 'T'])
                                vheatedb2_list = list(superheatedb2.loc[:, 'v'])
                                uheatedb2_list = list(superheatedb2.loc[:, 'u'])
                                hheatedb2_list = list(superheatedb2.loc[:, 'h'])
                                sheatedb2_list = list(superheatedb2.loc[:, 's'])
                            elif pressure_above == subcooled_pressures[l]:
                                superheateda2 = pd.read_excel(file_path3, l)
                                theateda2_list = list(superheateda2.loc[:, 'T'])
                                vheateda2_list = list(superheateda2.loc[:, 'v'])
                                uheateda2_list = list(superheateda2.loc[:, 'u'])
                                hheateda2_list = list(superheateda2.loc[:, 'h'])
                                sheateda2_list = list(superheateda2.loc[:, 's'])
                        theated2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(theatedb2_list),
                                                       list(theateda2_list))
                        vheated2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(vheatedb2_list),
                                                       list(vheateda2_list))
                        uheated2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(uheatedb2_list),
                                                       list(uheateda2_list))
                        hheated2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(hheatedb2_list),
                                                       list(hheateda2_list))
                        sheated2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(sheatedb2_list),
                                                       list(sheateda2_list))
                        h_b2, h_a2 = lb.above_below(h2, list(hheated2_list))
                        v_b2, v_a2 = lb.corresponding_ab(h2, hheated2_list, vheated2_list)
                        u_b2, u_a2 = lb.corresponding_ab(h2, hheated2_list, uheated2_list)
                        t_b2, t_a2 = lb.corresponding_ab(h2, hheated2_list, theated2_list)
                        s_b2, s_a2 = lb.corresponding_ab(h2, hheated2_list, sheated2_list)
                        v2 = lb.interpolate(h2, h_b2, h_a2, v_b2, v_a2)
                        u2 = lb.interpolate(h2, h_b2, h_a2, u_b2, u_a2)
                        t2 = lb.interpolate(h2, h_b2, h_a2, t_b2, t_a2)
                        s2 = lb.interpolate(h2, h_b2, h_a2, s_b2, s_a2)
                        print("Superheated Vapor\nv2 = " + str(v2) + " m^3/kg\nu2 = " + str(u2) + " kJ/kg\nT2 = " + str(
                            t2) + " C\ns2 = " + str(s2) + " K*kJ/kg")
    elif q_or_t == str("Q"):
        t2 = float(input("What is the temperature in C "))
        P2 = float(input("What is your ending pressure in kPa? "))
        m2 = float(input("What is your outlet mass flow rate in kg/s? "))
        if float(t2) in list(tsat_list):
            for i in range(len(tsat_list)):
                if float(tsat_list[i]) == float(t2):
                    p2_expect = float(psat_list[i])
        else:
            t2_b, t2_a = lb.above_below(float(t2), tsat_list)
            p2_b, p2_a = lb.corresponding_ab(float(t2), tsat_list, psat_list)
            p2_expect = lb.interpolate(t2, t2_a, t2_b, p2_a, p2_b)
        if P2 > p2_expect:
            # subcooled liquids
            if P2 in subcooled_pressures:
                for q in range(len(subcooled_pressures)):
                    if P2 == subcooled_pressures[q]:
                        subcooled2 = pd.read_excel(file_path3, q)
                        tcooled2_list = subcooled2.loc[:, 'T']
                        vcooled2_list = subcooled2.loc[:, 'v']
                        ucooled2_list = subcooled2.loc[:, 'u']
                        hcooled2_list = subcooled2.loc[:, 'h']
                        scooled2_list = subcooled2.loc[:, 's']
                if t2 in list(tcooled2_list):
                    index = lb.find_index(t2, hcooled2_list)
                    v2 = list(vcooled2_list)[index]
                    u2 = list(ucooled2_list)[index]
                    h2 = list(hcooled_list)[index]
                    s2 = list(scooled2_list)[index]
                    print("Subcooled Liquid\nv2 = " + str(v2) + " m^3/kg\nu2 = " + str(u2) + " kJ/kg\nT2 = " + str(
                        t2) + " C\ns2 = " + str(s2) + " K*kJ/kg")
                    Q = m2 * h2 - m1 * h1
                    print("Q = " + str(Q) + "kJ/s")
                else:
                    t_b2, t_a2 = lb.above_below(t2, list(tcooled2_list))
                    v_b2, v_a2 = lb.corresponding_ab(t2, tcooled2_list, vcooled2_list)
                    u_b2, u_a2 = lb.corresponding_ab(t2, tcooled2_list, ucooled2_list)
                    h_b2, h_a2 = lb.corresponding_ab(t2, tcooled2_list, hcooled2_list)
                    s_b2, s_a2 = lb.corresponding_ab(t2, tcooled2_list, scooled2_list)
                    v2 = lb.interpolate(t2, t_b2, t_a2, v_b2, v_a2)
                    u2 = lb.interpolate(t2, t_b2, t_a2, u_b2, u_a2)
                    h2 = lb.interpolate(t2, t_b2, t_a2, h_b2, h_a2)
                    s2 = lb.interpolate(t2, t_b2, t_a2, s_b2, s_a2)
                    print("Subcooled Liquid\nv2 = " + str(v2) + " m^3/kg\nu2 = " + str(u2) + " kJ/kg\nh2 = " + str(
                        h2) + " kJ/kg\ns2 = " + str(s2) + " K*kJ/kg")
                    Q = m2 * h2 - m1 * h1
                    print("Q = " + str(Q) + "kJ/s")
            elif P2 not in subcooled_pressures:
                pressure_below, pressure_above = lb.above_below(pressure, subcooled_pressures)
                for l in range(len(subcooled_pressures)):
                    if pressure_below == subcooled_pressures[l]:
                        subcooledb2 = pd.read_excel(file_path3, l)
                        tcooledb2_list = list(subcooledb2.loc[:, 'T'])
                        vcooledb2_list = list(subcooledb2.loc[:, 'v'])
                        ucooledb2_list = list(subcooledb2.loc[:, 'u'])
                        hcooledb2_list = list(subcooledb2.loc[:, 'h'])
                        scooledb2_list = list(subcooledb2.loc[:, 's'])
                    elif pressure_above == subcooled_pressures[l]:
                        subcooleda2 = pd.read_excel(file_path3, l)
                        tcooleda2_list = list(subcooleda2.loc[:, 'T'])
                        vcooleda2_list = list(subcooleda2.loc[:, 'v'])
                        ucooleda2_list = list(subcooleda2.loc[:, 'u'])
                        hcooleda2_list = list(subcooleda2.loc[:, 'h'])
                        scooleda2_list = list(subcooleda2.loc[:, 's'])
                tcooled2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(tcooledb2_list),
                                               list(tcooleda2_list))
                vcooled2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(vcooledb2_list),
                                               list(vcooleda2_list))
                ucooled2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(ucooledb2_list),
                                               list(ucooleda2_list))
                hcooled2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(hcooledb2_list),
                                               list(hcooleda2_list))
                scooled2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(scooledb2_list),
                                               list(scooleda2_list))
                t_b2, t_a2 = lb.above_below(t2, list(tcooled2_list))
                v_b2, v_a2 = lb.corresponding_ab(t2, tcooled2_list, vcooled2_list)
                u_b2, u_a2 = lb.corresponding_ab(t2, tcooled2_list, ucooled2_list)
                h_b2, h_a2 = lb.corresponding_ab(t2, tcooled2_list, hcooled2_list)
                s_b2, s_a2 = lb.corresponding_ab(t2, tcooled2_list, scooled2_list)
                v2 = lb.interpolate(t2, t_b2, t_a2, v_b2, v_a2)
                u2 = lb.interpolate(t2, t_b2, t_a2, u_b2, u_a2)
                h2 = lb.interpolate(t2, t_b2, t_a2, h_b2, h_a2)
                s2 = lb.interpolate(t2, t_b2, t_a2, s_b2, s_a2)
                print("Subcooled Liquid\nv2 = " + str(v2) + " m^3/kg\nu2 = " + str(u2) + " kJ/kg\nh2 = " + str(
                    h2) + " kJ/kg\ns2 = " + str(s2) + " K*kJ/kg")
                Q = m2 * h2 - m1 * h1
                print("Q = " + str(Q) + "kJ/s")
        elif float(P2) < float(p2_expect):
            print('yay')
            # Superheated Vapor
            if P2 in superheated_pressures:
                for q in range(len(list(superheated_pressures))):
                    if P2 == superheated_pressures[q]:
                        superheated2 = pd.read_excel(file_path2, q)
                        theated2_list = superheated2.loc[:, 'T']
                        vheated2_list = superheated2.loc[:, 'v']
                        uheated2_list = superheated2.loc[:, 'u']
                        hheated2_list = superheated2.loc[:, 'h']
                        sheated2_list = superheated2.loc[:, 's']
                if t2 in list(theated2_list):
                    index = lb.find_index(t2, hheated2_list)
                    v2 = list(vheated2_list)[index]
                    u2 = list(uheated2_list)[index]
                    h2 = list(hheated_list)[index]
                    s2 = list(sheated2_list)[index]
                    print("Superheated Vapor\nv2 = " + str(v2) + " m^3/kg\nu2 = " + str(
                        u2) + " kJ/kg\nh2 = " + str(
                        h2) + " kJ/kg\ns2 = " + str(s2) + " K*kJ/kg")
                    Q = m2 * h2 - m1 * h1
                    print("Q = " + str(Q) + "kJ/s")
                else:
                    t_b2, t_a2 = lb.above_below(t2, list(theated2_list))
                    v_b2, v_a2 = lb.corresponding_ab(t2, theated2_list, vheated2_list)
                    u_b2, u_a2 = lb.corresponding_ab(t2, theated2_list, uheated2_list)
                    h_b2, h_a2 = lb.corresponding_ab(t2, theated2_list, hheated2_list)
                    s_b2, s_a2 = lb.corresponding_ab(t2, theated2_list, sheated2_list)
                    v2 = lb.interpolate(t2, t_b2, t_a2, v_b2, v_a2)
                    u2 = lb.interpolate(t2, t_b2, t_a2, u_b2, u_a2)
                    h2 = lb.interpolate(t2, t_b2, t_a2, h_b2, h_a2)
                    s2 = lb.interpolate(t2, t_b2, t_a2, s_b2, s_a2)
                    print("Superheated Vapor\nv2 = " + str(v2) + " m^3/kg\nu2 = " + str(
                        u2) + " kJ/kg\nh2 = " + str(
                        h2) + " kJ/kg\ns2 = " + str(s2) + " K*kJ/kg")
                    Q = m2 * h2 - m1 * h1
                    print("Q = " + str(Q) + "kJ/s")
            elif P2 not in superheated_pressures:
                pressure_below, pressure_above = lb.above_below(pressure, superheated_pressures)
                for l in range(len(superheated_pressures)):
                    if pressure_below == superheated_pressures[l]:
                        superheatedb2 = pd.read_excel(file_path3, l)
                        theatedb2_list = list(superheatedb2.loc[:, 'T'])
                        vheatedb2_list = list(superheatedb2.loc[:, 'v'])
                        uheatedb2_list = list(superheatedb2.loc[:, 'u'])
                        hheatedb2_list = list(superheatedb2.loc[:, 'h'])
                        sheatedb2_list = list(superheatedb2.loc[:, 's'])
                    elif pressure_above == subcooled_pressures[l]:
                        superheateda2 = pd.read_excel(file_path3, l)
                        theateda2_list = list(superheateda2.loc[:, 'T'])
                        vheateda2_list = list(superheateda2.loc[:, 'v'])
                        uheateda2_list = list(superheateda2.loc[:, 'u'])
                        hheateda2_list = list(superheateda2.loc[:, 'h'])
                        sheateda2_list = list(superheateda2.loc[:, 's'])
                theated2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(theatedb2_list),
                                               list(theateda2_list))
                vheated2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(vheatedb2_list),
                                               list(vheateda2_list))
                uheated2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(uheatedb2_list),
                                               list(uheateda2_list))
                hheated2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(hheatedb2_list),
                                               list(hheateda2_list))
                sheated2_list = lb.interpolist(pressure, pressure_below, pressure_above, list(sheatedb2_list),
                                               list(sheateda2_list))
                t_b2, t_a2 = lb.above_below(t2, list(theated2_list))
                v_b2, v_a2 = lb.corresponding_ab(t2, theated2_list, vheated2_list)
                u_b2, u_a2 = lb.corresponding_ab(t2, theated2_list, uheated2_list)
                h_b2, h_a2 = lb.corresponding_ab(t2, theated2_list, theated2_list)
                s_b2, s_a2 = lb.corresponding_ab(t2, theated2_list, sheated2_list)
                v2 = lb.interpolate(t2, t_b2, t_a2, v_b2, v_a2)
                u2 = lb.interpolate(t2, t_b2, t_a2, u_b2, u_a2)
                h2 = lb.interpolate(t2, t_b2, t_a2, h_b2, h_a2)
                s2 = lb.interpolate(t2, t_b2, t_a2, s_b2, s_a2)
                print("Superheated Vapor\nv2 = " + str(v2) + " m^3/kg\nu2 = " + str(u2) + " kJ/kg\nh2 = " + str(
                    h2) + " kJ/kg\ns2 = " + str(s2) + " K*kJ/kg")
                Q = m2 * h2 - m1 * h1
                print("Q = " + str(Q) + "kJ/s")
# :)











