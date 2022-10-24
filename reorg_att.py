with open("attributs_ops.txt") as f:
    attributs_ops = f.readlines()
with open("attributs_event.txt") as f:
    attributs_event = f.readlines()
with open("business_name_ops.txt") as f:
    business_name_ops = f.readlines()

provided = [
    "turmmxu4.a.phsa.cval.mag.f",
    "turmmxu4.a.phsb.cval.mag.f",
    "turmmxu4.a.phsc.cval.mag.f",
    "turmmxu4.hz.mag.f",
    "turmmxu4.pnv.phsa.cval.mag.f",
    "turmmxu4.pnv.phsb.cval.mag.f",
    "turmmxu4.pnv.phsc.cval.mag.f",
    "turmmxu4.totpf.mag.f",
    "wgen4.brgtmp1.mag.f",
    "wgen4.brgtmp2.mag.f",
    "wgen4.inlettmp.mag.f",
    "wgen4.rotspd.mag.f",
    "wgen4.stttmp3.mag.f",
    "wmet4.envtmp.mag.f",
    "wmet4.horwdspd.mag.f",
    "wnac4.dir.mag.f",
    "wnac4.intntmp.mag.f",
    "wrot4.blpthangtgt1.mag.f",
    "wrot4.blpthangtgt2.mag.f",
    "wrot4.blpthangtgt3.mag.f",
    "wrot4.blpthangval1.mag.f",
    "wrot4.blpthangval2.mag.f",
    "wrot4.blpthangval3.mag.f",
    "wrot4.rotspd.mag.f",
    "wtrf4.gritmp2.mag.f",
    "wtrf4.gritmp3.mag.f",
    "wtrm4.gbxoiltmp.mag.f",
    "wtrm4.rotbrgtmp.mag.f",
    "wtrm4.shftbrgtmp2.mag.f",
    "wtur4.var.mag.f",
    "wtur4.w.mag.f",
]

all_attrib_ops = [i for i in attributs_ops if i != "\n"]
all_attrib_ops = [i.strip().replace("\n", "").lower() for i in all_attrib_ops]
all_attrib_ops_clean = [i for i in all_attrib_ops if not i.endswith("*")]

all_attrib_event = [i for i in attributs_event if i != "\n"]
all_attrib_event = [i.strip().replace("\n", "").lower() for i in all_attrib_event]
all_attrib_event_clean = [i for i in all_attrib_event if not i.endswith("*")]

extra_attrib_ops = [i for i in all_attrib_ops if i.endswith("*")]
extra_attrib_ops = [i.replace("*", "") for i in extra_attrib_ops]

extra_attrib_event = [i for i in all_attrib_event if i.endswith("*")]
extra_attrib_event = [i.replace("*", "") for i in extra_attrib_event]

all_business_name_ops = [i for i in business_name_ops if i != "\n"]
all_business_name_ops = [i.strip().replace("\n", "").lower() for i in all_business_name_ops]
all_attrib_ops = [i.replace("*", "") for i in all_attrib_ops]
zip_iterator = zip(all_business_name_ops, all_attrib_ops)
mapping_dict = dict(zip_iterator)
# print(mapping_dict)

test = "lala"
tt = "lolo"

print("-".join([tt, test]))
