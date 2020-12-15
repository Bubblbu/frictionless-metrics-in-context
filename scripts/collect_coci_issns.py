from pathlib import Path

import pandas as pd
from habanero import Crossref
from tqdm import tqdm

data_dir = Path(__file__).parent.parent.absolute() / "data"
nb_dir = data_dir / "coverage"

# Download COCI coverage
cr = Crossref()

limit = 1000
n_members = cr.members(filter={"has-public-references": "true"}, limit=0)["message"][
    "total-results"
]

offsets = list(range(0, n_members, 1000))

items = []
for offset in tqdm(offsets):
    r = cr.members(filter={"has-public-references": "true"}, limit=limit, offset=offset)
    items.extend(r["message"]["items"])

df = pd.DataFrame.from_records(items)
df.to_json(nb_dir / "coci/depositing_members.jsonl", lines=True, orient="records")
