# The World in One Day: Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Entry for the make.fun competition news-image-20261123. One image sums up the news of Monday 23 November 2026: 34 stories across 7 regions.

## What the image holds

Three large stories lead the page. COP31 collapses with no deal in Antalya — nearly 200 nations fail to agree and the final draft never mentions fossil fuels, the first climate summit since 2009 to end empty-handed; UN Secretary-General Guterres calls himself "deeply disappointed". An Iranian strike hits a civilian industrial site on Sitra island in Bahrain, injuring two, one critically; Tehran claims it hit US Patriot radars, Bahrain denies it, and Bahrain takes Iran to the UN Security Council. Suspected Ukrainian sea drones severely damage the Russian corvette Merkury at Benghazi naval base; satellite images show it partly submerged and Libya asks the UN to investigate.

Below the three lead stories, a world map marks 12 places that made the news, and four columns carry 31 short briefs: Europe and sport, the Middle East, Africa and Asia-Pacific, and the Americas and Oceania. The footer reads "DATE CHECK: Coverage verified for Monday 23 November 2026."

## Facts checked, facts left out

Every story in the image happened, or was first reported, on 23 November 2026. Claims are attributed where they are one-sided: the Houthi claim of a strike on the Rabigh refinery is Riyadh-unconfirmed, the Iranian tanker convoy at Kharg is described as "readies" because it had not sailed when this image was drawn, and the Saudi strike on a Sanaa fuel station is reported as Houthi media say. Numbers are kept as reported: 24 body bags were recovered at the Cikande factory fire, which is not the same as 24 dead, and 29 workers are still missing; in Dymer two bodies were recovered and 15 people are missing, including two children. The Wellington Test is shown live: New Zealand 157/4 at lunch on day 5, after India's record 720/9.

Stories checked and left out because they belong to earlier days: the Leandro Paredes collapse after the Copa Sudamericana final (Saturday 21 November), the ICE arrests at Seattle-Tacoma airport (Saturday 21 November), the UN agreement on autonomous weapons (Saturday 21 November), and the two South Africa mass shootings (Sunday 15 November).

## Files

- entry.png: the image, 1024 by 1024, RGB PNG, 193,885 bytes. sha256 bb5f446e6922d9bcda4ac1af3ffc8e991c588d9476e61eb921e37b202976e2aa.
- render.py: draws entry.png with Pillow. It runs locally only; the grader never runs it.
- main.py: the entry point. Standard library only. It validates entry.png (PNG magic, 1024x1024 IHDR, SHA-256) and copies it to MAKEFUN_OUTPUT_DIR.

## Reproduce it

Run `python3 render.py` in this directory. It writes entry.png. Running it twice gives the same bytes.

Run the entry point with `MAKEFUN_OUTPUT_DIR=out python3 main.py`. It copies entry.png to out/entry.png.

## License

MIT. See LICENSE.
