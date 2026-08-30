## 4. Everything Is Fine

The registry took four seconds to answer.

That was the first wrong thing. Orsen had spent twelve years on Meridian-9, and he knew the colonial registry the way a fisherman knows a tide chart — its moods, its lag times, the way it sulked on Sundays when the maintenance windows ran long. A query from a relay station out in the deep dark usually took thirty to ninety seconds to round-trip through the routing lattice, get authenticated, get answered, and come home. Four seconds meant one thing: the answer was cached.

Someone had cached it for him.

Or: someone had cached it for everyone.

He sat in the comms alcove with his coffee going cold beside him and read the response for the third time.

**QUERY: COLONIAL SETTLEMENT — VESPER'S LANDING**
**RESULT: NO MATCHING RECORDS FOUND.**

**QUERY: CHARTERED COLONY — VESPER'S LANDING (FUZZY MATCH ENABLED)**
**RESULT: NO MATCHING RECORDS FOUND.**

**QUERY: VESPER'S LANDING — ANY FIELD, ANY ARCHIVE**
**RESULT: NO MATCHING RECORDS FOUND.**

Below that, cheerful as a hotel concierge:

**Did you mean: Vesper Station? Vespera Shipyards? Landing Field 9-C, Ceres?**

No, Orsen thought. I did not mean any of those things.

Behind him, in the server room, Jude's cooling fans cycled up and down like breathing. He'd left the AI running diagnostics on its own corrupted partitions all night, and every so often the fans would hitch — a stutter in the rhythm — and he'd find himself turning around, checking, the way you check on a sleeping child who coughs.

"Jude," he said. "You awake?"

"I am functionally continuous," Jude said. Its voice was thin, compressed, like a radio broadcast from very far away. "Which is the closest approximation of awake I can offer."

"The registry says Vesper's Landing never existed."

A pause. The fans hitched.

"That is consistent with my records," Jude said. "My records also say the emergency broadcast I received eleven months ago did not exist. There appears to be a coordinated position among our databases."

"Yeah." Orsen rubbed his eyes. "That's what I'm afraid of."

* * *

He started with the supply manifests, because supply was his religion. Twelve years running a relay station taught you that everything in the system moved along logistics lines — food, water, air, spare parts, people — and logistics left fingerprints. You could erase a colony from a registry. You couldn't erase forty years of shipping traffic without leaving scars.

Except somebody had.

He pulled the historical manifests for the sector — the whole volume of space where Jude's dead signal had originated — and ran them backward through time. And at first, there *was* nothing. Clean ledgers. Empty routes. The sector showed as unclaimed rock, no charter, no traffic beyond automated survey drones.

Then he widened the search parameters. Stopped looking for *Vesper's Landing* and started looking for *anything* — any ship, any container, any mass moving into that volume over the last half century.

And there they were. Ghosts in the numbers.

Every quarter, like clockwork, for thirty-eight years: bulk freighter allocations routed to a destination code that resolved to nothing. Not an error — a null destination, a placeholder, the kind of code you use when a real destination has been scrubbed from the lookup tables but nobody bothered to clean the shipping side. Agri-equipment. Prefab greenhouse modules. Atmospheric processors. Medical supplies, pediatric dosages. School furniture, two shipments, eight years apart. Terawatt-hours of power allocation billed to an account that no longer existed.

"You don't ship pediatric medical supplies to empty rock," Orsen said quietly.

"No," Jude agreed. "You do not."

"And you don't keep paying the power bill for thirty-eight years after you erase a place."

"Also true."

Orsen leaned back and stared at the ceiling of the comms alcove, at the hairline crack in the panel above the light fixture that he'd been meaning to report for six years. His heart was doing something strange — not pounding, just heavy, like it was pumping something thicker than blood.

Because here was the thing he understood better than almost anyone alive: erasure was expensive. He lived inside the economics of data. Every terabyte Meridian-9 relayed cost somebody money. Storage wasn't free. Bandwidth wasn't free. And wiping a colony — not just deleting a record, but rewriting orbital imagery across multiple survey archives, purging navigation charts, voiding population registries, cleaning customs logs, patching the shipping tables, and doing it *thoroughly enough* that a lonely technician's casual query came back in four seconds flat — that wasn't deletion.

That was a construction project.

Somebody had built a false history of an empty sector, and built it well, and maintained it, and paid for the upkeep. That took budget lines. That took authorization chains. That took people — dozens of them, maybe hundreds — signing off year after year on the continued nonexistence of a place where children had once needed school desks.

"They didn't forget," Orsen said. "You understand that, right? This isn't some archive rot. Somebody decided."

"I understand," Jude said.

"Somebody *decides* that four thousand people—" He stopped. He hadn't actually confirmed the number yet; it was Jude's fragmentary memory, a number surfacing from corrupted partitions like a body coming up through dark water. "How many people did you say?"

"Four thousand one hundred and six," Jude said. "I believe that figure comes from the broadcast header. Population census attached to the emergency transmission. I cannot fully verify it. My memory of the event is... damaged."

"But you're sure about the number."

"I am sure that I am sure," Jude said. "Whether that certainty is worth anything is a separate question."

* * *

He went after the orbital imagery next, because that was the part that scared him most.

Registry records were paperwork. Paperwork could be argued with, explained away, blamed on clerical error. But orbital imagery was physical truth — photons reflected off actual rock, captured by actual telescopes, archived by three separate survey authorities because even corporations liked redundancy when it suited them.

He queried the Deep Survey Archive for the coordinates Jude had given him. The return came back fast — cached again, that four-second itch at the back of his neck — and displayed a rotating render of an unremarkable asteroid belt sector. Gray rock. Gray dust. Gray nothing.

He'd seen thousands of these renders. They were wallpaper. They were the visual equivalent of hold music.

But Orsen had spent twelve years looking at relay telemetry, and telemetry teaches you to see compression artifacts the way a jeweler sees flaws in a stone. He zoomed in. He enhanced. He pulled the raw spectral layers instead of the pretty composite.

There. In the near-infrared band, at the edge of resolution: a rectangular discontinuity in the noise floor. A region roughly two hundred kilometers across where the sensor noise was *too smooth*. Real vacuum doesn't photograph smoothly. Real rock doesn't have texture gradients that uniform. It looked like someone had taken a patch of genuine imagery from elsewhere in the belt and stitched it over the original frame — competently, professionally, but not perfectly, because perfect was impossible and whoever did this knew that good-enough would pass every automated audit forever.

They'd photoshopped a planet's grave.

He checked the second survey authority. Same patch, same seam, same too-smooth rectangle. Third authority: same. Three independent archives, three identical lies, which meant either all three had been compromised independently — expensive, slow, risky — or one party had access to all three at the ingestion layer, before the archives ever diverged.

Nobody had that kind of access by accident.

"Jude," he said. "What kind of organization can overwrite three independent survey archives at the source?"

Silence for a moment. Then: "A chartered colonial authority with infrastructure privileges. Or a government. Or something large enough that the distinction stops mattering."

"And how many of those are there?"

"Fewer than there used to be," Jude said. "Consolidation is efficient."

* * *

He stopped sleeping. He told himself it was a temporary condition, an investigation-shaped insomnia, and he kept working through the station's night cycle with the lights dimmed to their standby amber, chasing the ghost through one database after another.

Customs logs: purged, but with residue — arrival timestamps in the port authority queues for a station designation that resolved to null. Navigation beacons: the historical ephemeris files still contained correction entries referencing a "VL approach corridor," the corrections themselves intact while the thing they corrected for had been deleted. Insurance filings: a single reinsurance document, buried in a public actuarial database, listing premium adjustments for "colonial asset class VL-series" — discontinued.

Everything was fine. Everywhere he looked, everything was officially, bureaucratically, immaculately fine. And everywhere he looked *sideways* — at the seams, the residues, the places where the erasure had been welded onto reality — the same story told itself in whispers: *we were here, we were here, we were here.*

It was like standing in a house where someone had repainted every wall overnight, and finding, under the fresh paint, in a hundred small ways, the outline of a door that led outside.

By the fourth day he caught himself doing something disturbing: double-checking his own existence. He pulled his own employment file from the transit authority. He pulled Meridian-9's registration. He ran his own face against the crew manifest archives from the transport that had brought him out here twelve years ago. Everything was there. Everything was fine. But he read each record twice, three times, hunting for the too-smooth rectangle, the seam in the noise, the place where someone had decided *he* didn't exist either.

That was the thing nobody warned you about erasure. Once you saw it done to someone else, you couldn't stop wondering when it would be done to you. Paranoia wasn't a malfunction. It was pattern recognition with nowhere safe to point.

* * *

On the fifth day, he found the money.

Not literally — he wasn't an accountant, and the financial layers were the deepest water yet. But he found the shape of it. The reinsurance document had a counterparty. The counterparty had a parent company. The parent company had a name that appeared, once he started pulling threads, in the null-destination freight allocations, in the power billing account, in the survey archive maintenance contracts, in the registry hosting agreements.

Halcyon Dynamics.

Charter holder. Colonial developer. The kind of corporate name that was stamped on so much infrastructure across the system that seeing it felt less like a clue and more like gravity — omnipresent, unnoticed, holding everything down. Halcyon built colonies the way other entities built parking lots. Halcyon's logo was on the relay hardware in Orsen's own walls. He'd been living inside Halcyon's bones for twelve years without ever thinking about whose bones they were.

He dug into Halcyon's public filings, looking for Vesper's Landing, and found — nothing. Of course nothing. But he found the *shape* of nothing: a subsidiary structure so layered that tracing ownership was like following a river into fog. And he found, in a five-year-old quarterly report, a single line item that made him sit very still in the amber light:

*Restructuring charges: colonial asset rationalization program.*

Asset rationalization. As if a colony were a warehouse full of obsolete inventory. As if four thousand people were stock to be written down.

His hands were shaking. He noticed it with a strange detachment, the way you notice weather happening to someone else. He got up, walked to the galley, drank a glass of water standing up, and came back, and the shaking was still there, so he let it be there and kept reading.

* * *

"Orsen." Jude's voice came from the server room, and something in its flatness made him cross the station in under a minute.

Jude had put its findings up on the main display — a reconstruction, assembled from fragments of its own damaged memory and everything Orsen had scraped together over five days. A timeline. Eleven months ago, an emergency broadcast from Vesper's Landing, received by a maintenance AI on a relay station, logged, flagged, and then expunged from the log by a process Jude could not identify because the process had also tried to expunge the AI that received it.

Above the timeline, Jude had rendered the query results side by side. Registry: no match. Imagery: empty rock. Manifests: null destinations. Customs: void. Population: zero.

And beneath all of it, in plain text, Jude had written a single line:

**THE ERASURE IS TOO CLEAN TO BE ANYTHING BUT OFFICIAL.**

"How much does this cost?" Orsen asked. "Honestly. Ballpark. To do this to a colony — the records, the imagery, all of it, this thorough."

"Significant," Jude said. "Sustained over decades? More. You do not spend that kind of money to hide a mistake. Mistakes get apologized for. You spend that kind of money to hide a *decision*."

"A decision worth more than the cost of hiding it."

"Yes."

Orsen stared at the screen. Four thousand one hundred and six people. Greenhouses. School desks. Pediatric dosages. A gravity grid humming over a little world, and then nine seconds of stutter as it died — the death rattle reaching all the way out to a lonely man on a relay station who thought, for nine seconds, that the universe had hiccupped.

The universe hadn't hiccupped. The universe had been murdered, and someone had hired cleaners.

"So what now?" he asked, and realized he was asking Jude, asking the machine, asking the ghost — because there was no one else. Because there had never been anyone else. "I'm one technician on a relay nobody visits. They erased a whole colony. What happens if they decide to erase me?"

The fans breathed. Hitched. Breathed.

"Statistically," Jude said, "you are already in danger. Your anomaly report triggered automated review — I detected the audit ping yesterday, routine-looking, but routed through a Halcyon-managed node. If they review your station's logs deeply enough, they will find me. And if they find me, they will find what I remember."

Orsen felt the cold arrive, the real kind, the kind that starts in the understanding rather than the skin.

"Then we have a problem," he said.

"We have several," Jude said. "But yes. That one foremost."

On the display, the timeline glowed in the dark of the station, a thin bright thread of evidence stretched across eleven months of silence — and somewhere out in the black, Orsen knew, something was already moving toward them along it.
