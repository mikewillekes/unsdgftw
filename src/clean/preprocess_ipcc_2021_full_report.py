from config import config
import re

"""
    !!!After running TIKA on IPCC_AR6_WGI_Full_Report.pdf - you need to run this cleanup script!!!

    The full file /corpus/IPCC/1-raw/IPCC_AR6_WGI_Full_Report.pdf (from https://www.ipcc.ch/report/ar6/wg1/) has a format where
    every line in the PDF has a number; this manifests in the Tika XHML file like this:

        <p> 1 
        2 
        </p>
        <p> 3 
        Figure TS.13: Estimates of the net cumulative energy change (ZJ = 1021 Joules) for the period 1971–2018 4 
        </p>
        <p>associated with: (a) observations of changes in the Global Energy Inventory (b) Integrated 5 
        Radiative Forcing; (c) Integrated Radiative Response. The intent is to show assessed changes in 6 
        energy budget and ERFs. Black dotted lines indicate the central estimate with likely and very likely 7 
        ranges as indicated in the legend. The grey dotted lines indicate the energy change associated with an 8 
        estimated pre-industrial Earth energy imbalance of 0.2 W m-2 (panel a) and an illustration of an 9 
        assumed pattern effect of –0.5 W m–2 °C–1 (panel c). Background grey lines indicate equivalent 10 
        heating rates in W m–2 per unit area of Earth’s surface. Panels (d) and (e) show the breakdown of 11 
        components, as indicated in the legend, for the Global Energy Inventory and Integrated Radiative 12 
        Forcing, respectively. Panel (f) shows the Global Energy Budget assessed for the period 1971–2018, 13 
        that is,  the consistency between the change in the Global Energy Inventory relative to pre-industrial 14 
        and the implied energy change from Integrated Radiative Forcing plus Integrated Radiative Response 15 
        under a number of different assumptions, as indicated in the figure legend, including assumptions of 16 
        correlated and uncorrelated uncertainties in Forcing plus Response. Shading represents the very likely 17 
        range for observed energy change relative to pre-industrial and likely range for all other quantities. 18 
        Forcing and Response timeseries are expressed relative to a baseline period of 1850–1900.  19 
        </p>
        <p>  20 
        21 
        22 
        </p>
        <p>  23 
        </p>
        <p>ACCEPTED VERSION

    Notice how each line ends in an incrementing number...

    This helper script pre-processes that file and strips out the line-index numbers
"""

pattern = r'([ -])([0-9]{1,3}) \n'
substitution = r'\1 \n'

filename = f'{config.CORPUS_DIR}/IPCC/{config.TEXT_DIR}/IPCC_AR6_WGI_Full_Report.pdf.xml'

orig_lines = []
cleaned_lines = []

with open(filename, 'r') as fin:
    for line in fin:
        orig_lines.append(line)
        cleaned_lines.append(re.sub(pattern, substitution, line))

# Write the original file to a backup
with open(filename + '.bak', 'w') as fout:
    fout.writelines(orig_lines)

# Overwrite the original file
with open(filename, 'w') as fout:
    fout.writelines(cleaned_lines)