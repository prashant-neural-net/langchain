# web-page loader

from langchain_community.document_loaders import WebBaseLoader

url = "https://www.amazon.in/Haldirams-Delhi-Samosa-200g/dp/B0024VCYCK/ref=sr_1_6_in_f3_0o_fs_mod_primary_alm?dib=eyJ2IjoiMSJ9.epd6SAn2uFRMdzrxR0lwxXhTAcuhIWMe2nrtSzbcVAKrpW58rMRts8oksi1GXy_VJdCTxOXlXNgsnvDY9zr1lQCjPZIrvk-6MEcvWg5OfCfVB0BBAuLzdQILWQYDDiD1NiR5BObZS_f9mm2cbvzXcEwidMc4QUSGGIzoFkOPwJVttiXIm_QhP-aik2SrermuIsIBp8Tu71Q_RP2xiaMzD4VA4O76FevmW7K2Sd31Mc2Z-4rLnPZ26Yrgcgwc0R0DfIHG5844le98TL30e4trkcGmqc3JzxhqiztRCbVmT00.vrWKPEBsFGQSgIPlbWQMWqUwwer2mN0VMRdDPeqZP80&dib_tag=se&keywords=samosa&qid=1789901756&sbo=m6DjfpMzMLDmL8pSMKX8hw%3D%3D&sr=8-6"

loader = WebBaseLoader(url)

docs = loader.load()

print(docs[0].page_content)
