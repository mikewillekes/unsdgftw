
import spacy
from collections import Counter

texts = [
    'Potts, S. G., Imperatriz-Fonseca, V., Ngo, H. T., Aizen, M. A., Biesmeijer, J. C., Breeze, T. D., Dicks, L. V., Garibaldi, L. A., Hill, R., Settele, J., & Vanbergen, A. J.. Safeguarding pollinators and their values to human well-being. Nature, 540(7632), 220229. https://doi. org/10.1038/nature20588',
    'Powell, B., Thilsted, S. H., Ickowitz, A., Termote, C., Sunderland, T., & Herforth, A.. Improving diets with wild and cultivated biodiversity from across the landscape. Food Security, 7(3), 535554. https://doi.org/10.1007/s12571- 015-0466-5',
    'Johnson, H. E., Banack, S. A., & Cox, P. A.. Variability in Content of the Anti-AIDS Drug Candidate Prostratin in Samoan Populations of Homalanthus nutans. Journal of Natural Products, 71(12), 2041-2044, doi:10.1021/np800295m.',
    'Foley, J. A., DeFries, R., Asner, G. P., Barford, C., Bonan, G., Carpenter, S. R., Chapin, F. S., Coe, M. T., Daily, G. C., Gibbs, H. K., Helkowski, J. H., Holloway, T., Howard, E. A., Kucharik, C. J., Monfreda, C., Patz, J. A., Prentice, I. C., Ramankutty, N., & Snyder, P. K.. Global consequences of land use. Science, 309(5734), 570574. https://doi. org/10.1126/science.1111772',
    'Hunt, D. V. L., Lombardi, D. R., Atkinson, S., Barber, A. R. G., Barnes, M., Boyko, C. T., Brown, J., Bryson, J., Butler, D., Caputo, S., Caserio, M., Coles, R., Cooper, R. F. D., Farmani, R., Gaterell, M., Hale, J., Hales, C., Hewitt, C. N., Jankovic, L., Jefferson, I., Leach, J., MacKenzie, A. R., Memon, F. A., Sadler, J. P., Weingaertner, C., Whyatt, J. D., & Rogers, C. D. F.. Scenario Archetypes: Converging Rather than Diverging Themes. Sustainability, 4(12), 740 772. https://doi.org/10.3390/su4040740',
    'Nelson, M. C., Ingram, S. E., Dugmore, A. J., Streeter, R., Peeples, M. A., McGovern, T. H., Hegmon, M., Arneborg, J., Kintigh, K. W., Brewington, S., Spielmann, K. A., Simpson, I. A., Strawhacker, C., Comeau, L. E. L., Torvinen, A., Madsen, C. K., Hambrecht, G., & Smiarowski, K.. Climate challenges, vulnerabilities, and food security. Proceedings of the',
    'Chapter 3 addresses the questions of How much progress has been made towards the Aichi Biodiversity Targets and the objectives of other biodiversity-related agreements, and how do nature and its contributions to people contribute to the implementation of the Sustainable Development Goals? Building upon findings from chapter 2 and additional evidence from analyses of indicators and literature reviews, the chapter assesses progress towards meeting major international objectives related to biodiversity and sustainable development, with special attention given to the Aichi Biodiversity Targets and to relevant Sustainable Development Goals. The chapter also examines the objectives of other biodiversity- related agreements: Convention on Migratory Species, Convention on International Trade in Endangered Species, Ramsar Convention on Wetlands, Convention to Combat Desertification, World Heritage Convention, International Plant Protection Convention, Convention on the Conservation of',
    'A global assessment of the health and benefits of the oceans suggest that ocean health requires significant improvement to achieve major goals including several of the SDGs. Global scale assessments of the health of individual marine ecosystems also generally detail major declines over the last 20 50 years, with significant regional variability. For example, kelp ecosystems have experiences declines in abundance in 38% of ecoregions, increases in 27% of ecoregions, and no detectable change in 35% of ecoregions. In other ecosystems, the declines are more consistent and pervasive. Mangrove ecosystems have declined in global extent by about 38% by 2010, with an estimated loss of 40% of mangroves over the last 30 years in Indonesia, which has the greatest extent worldwide. Recent work suggests these deforestation rates may be slowing, but mangroves are still declining at a rate of approximately 0.18% per year on average across Southeast Asia. There is considerable variability among countries in deforestation rates, with the highest losses in Myanmar, Indonesian Sumatra and Borneo, and Malaysia. Seagrass ecosystems have experienced similar declines with historical loss rates of 30% and estimates of 7% loss per year since 1990. Tracking global and regional trends in the status of most marine ecosystems remains challenging, particularly for ecosystems that require regular field sampling, including',
]


nlp = spacy.load('en_core_web_trf')
is_using_gpu = spacy.prefer_gpu()
print (f'Using GPU: {is_using_gpu}')



for text in texts:
    """

    We want to be able to identify paragraphs of unstructured prose that are good candidates
    for sentence segmentation and NLP.
    This is a simple, rules-based way to use Part-of-Speech tagging and simple hueristics to identify

    a paragraph that is likely a references block:

        Powell, B., Thilsted, S. H., Ickowitz, A., Termote, C., Sunderland, T., & Herforth, A.. Improving diets with wild and
        cultivated biodiversity from across the landscape. Food Security, 7(3), 535554.
        https://doi.org/10.1007/s12571- 015-0466-5
        Counter({'PUNCT': 17, 'PROPN': 15, 'NUM': 7, 'NOUN': 3, 'ADP': 3, 'CCONJ': 2, 'ADJ': 2, 'VERB': 1, 'DET': 1, 'X': 1})

    vs.

        Chapter 3 addresses the questions of How much progress has been made towards the Aichi Biodiversity Targets and the
        objectives of other biodiversity-related agreements, and how do nature and its contributions to people contribute to
        the implementation of the Sustainable Development Goals? Building upon findings from chapter 2 and additional evidence
        from analyses of indicators and literature reviews, the chapter assesses progress towards meeting major international
        objectives related to biodiversity and sustainable development, with special attention given to the Aichi Biodiversity
        Targets and to relevant Sustainable Development Goals. The chapter also examines the objectives of other biodiversity-
        related agreements: Convention on Migratory Species, Convention on International Trade in Endangered Species, Ramsar
        Convention on Wetlands, Convention to Combat Desertification, World Heritage Convention, International Plant Protection
        Convention, Convention on the Conservation of
        Counter({'PROPN': 34, 'NOUN': 27, 'ADP': 21, 'PUNCT': 13, 'VERB': 12, 'DET': 10, 'ADJ': 9, 'CCONJ': 7, 'SCONJ': 3, 'AUX': 3, 'NUM': 2, 'PRON': 1, 'ADV': 1, 'PART': 1})

    Apply POS Tagging and then look at the ratio of PUNCT and PROPN
    """

    print ('--------------------------------------------')
    nlp_doc = nlp(text)
    pos_tokens = [token.pos_ for token in nlp_doc] 
    counter = Counter(pos_tokens)

    print(text)
    print(counter)
    print(f'text:{len(text)}\t PROPN:{counter["PROPN"]}\t PUNCT:{counter["PUNCT"]}\t total tokens:{len(pos_tokens)}')

    score = 1 - (counter['PROPN'] + counter['PUNCT']) / len(pos_tokens)
    print(score)
    