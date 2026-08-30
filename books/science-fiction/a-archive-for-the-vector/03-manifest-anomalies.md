## 3. Manifest Anomalies

The audit was supposed to take an hour.

Hazel had built the ritual herself, three years back, after a customs dispute on Calloway Ring nearly cost her the *Kestrel's* docking rights. Once a month, she sat down with her own ledgers and read them like a stranger would — every manifest, every fuel purchase, every berth fee, every bribe dressed up as a "handling surcharge." A hauler who couldn't pass a stranger's audit was a hauler waiting to be eaten. She'd learned that lesson in blood that wasn't technically hers, though she'd never been able to explain to anyone why she felt it so personally.

So on the fourth morning after Vesper's confessions, with the station humming its usual indifferent hum around her berth and two cups of recycled coffee going cold at her elbow, Hazel Whitlock opened her shipping records and started looking for the fire nobody reported.

She told herself it was coincidence. Vesper had named coordinates. She'd checked them against her charts at 0300 and found nothing there but empty space and an old navigational buoy long since dead. The Meridian's last position — if that's what the numbers were — sat in a volume of space no legitimate ship had reason to visit. She wasn't going to think about it. She was going to do her books.

Line by line. Month by month. Back through the quarter.

It took her forty minutes to find the first anomaly, and when she found it, she laughed out loud, alone in the cabin, because the alternative was something worse than laughing.

*Freight class 4-C, biological preservation, 1.2 cubic meters, origin: Meridian Station Annex, destination: Kestrel, hold B.*

Meridian Station Annex didn't exist. She knew every station on her routes the way other people knew the rooms of their childhood homes, and there was no annex, had never been an annex. And the date on the entry was eleven months ago — eleven months during which she had personally signed off on every crate that had entered or left her holds, because she never let dockhands touch her manifests, because manifests were where smugglers got caught and honest haulers got framed.

Except this one hadn't come through her hands. It had come through her *codes*.

Her authorization hash sat at the bottom of the entry, clean and valid, generated from her private key. Not forged — forged hashes were a thing she could spot; she'd spent money she didn't have on a verification suite precisely so she could spot them. This one verified. Which meant either her key had leaked, or someone had used it, or —

Or she had used it, and didn't remember.

Hazel set down the coffee cup very carefully, as if the cabin might pitch without warning, and pulled up the entry's full routing history.

*Origin: Meridian Station Annex.* The name sat there like a bruise. Eleven months ago she'd been running ore out of Thessaly Gate, three systems away. She remembered that run. She remembered the loadmaster with the twitchy eye, the solar storm that had delayed her departure for six hours, the bad noodles at the gate canteen. She remembered it in the specific, textured way she remembered everything — which was to say, completely, and only when she went looking.

She scrolled. There were more.

Seven entries over fourteen months. All class 4-C, all small — under two cubic meters each, the kind of cargo you could tuck behind a coolant manifold and forget. All routed through the Kestrel. All authorized under her hash. All originating from stations whose names were either wrong or subtly, horribly almost-right: Meridian Station Annex. Meridian Relay. New Meridian Transfer Point.

There was no such place as New Meridian. There had been a Meridian once. Everyone in the trade knew the story — colony ship lost with all hands in the opening weeks of the war, one of the atrocities both sides still traded accusations over. A whole generation of stations and relays had been named for it afterward, grief turned into signage. But not these. These names weren't memorials. They were *corrections*, like someone kept trying to spell a word and couldn't quite get it right.

And every single shipment had terminated at the Kestrel. Not delivered onward. Not picked up. Just — received. Into her hold. By her codes.

She stood up. Sat back down. Stood up again and paced the four meters of floor between the galley unit and the nav console, which was the entire geography of her home, and thought: *someone has been using my ship as a dead drop for a year, and I never noticed, and that is impossible, because I notice everything, noticing is the one thing I am.*

Then she thought the other thing. The thing she'd been not-thinking since 0300.

*Or I'm the someone, and I don't remember.*

* * *

The memories came the way weather came to the outer colonies — without forecast, without mercy.

She was standing at the galley, hands around a cup she wasn't drinking, when the first one arrived. Not a flashback exactly; she'd heard veterans describe flashbacks, the full sensory hijack of it, and this wasn't that. This was quieter and more obscene. It was more like remembering something that had happened yesterday, except it hadn't happened yesterday, and possibly it hadn't happened at all.

A corridor. White panels, the specific white of military fabrication, not civilian. Her boots making a sound on the deck that civilian boots didn't make — heavier, cadenced, part of something. Someone walking beside her saying, *"You'll want to review the order before you sign, Whitlock. Nobody signs this without reading it twice."*

And herself answering — her own voice, she could hear it, the exact timbre of it — *"I've read it twice. I just don't understand how it's legal."*

*"That's not the question you're being paid to ask."*

Gone. Like a door closing. Hazel stood in her galley with cold coffee and a heartbeat she could hear in her ears, and made herself say out loud, to the empty cabin: "I have never worn a uniform."

The cabin did not agree or disagree. That was the problem with cabins.

She tried to file it. She was good at filing things — she'd had ten years of practice burying the question of her own provenance under schedules and fuel math and the small daily tyranny of keeping a ship alive. Ten years ago she had woken up in a salvage bay with no records, no registry entry, no history older than the clothes she'd been found in, and she had made a decision that had worked beautifully right up until this morning: don't ask. Don't dig. Be the woman the paperwork says you are, even if the paperwork says almost nothing. Invisibility as survival. A person with no past can't be traced to one.

But the memory had her voice in it. And the voice had said *Whitlock* like it was a name people used in rooms with white walls.

She went back to the console because sitting still was worse, and because the records were the one thing in her life that obeyed rules. Data didn't lie. Data didn't arrive unbidden wearing her own voice. She pulled the seven anomalous entries into a timeline and made herself look at their spacing.

Fourteen months. Seven shipments. Roughly every sixty days, give or take — and then she saw it, and her stomach dropped through the deck plates and kept going.

The intervals weren't sixty days. They were sixty days *minus the length of whatever run she'd been on*. The shipments hadn't arrived on a schedule. They had arrived whenever the Kestrel was docked. Whenever *she* was docked. Every single one had been received within hours of her arrival at a berth, timed so precisely that whoever — or whatever — was sending them had known her ETA before she did.

Nobody knew her ETA before she filed it. Filing flight plans early was the first rule of staying invisible; she filed late, always, sometimes minutes before burn.

Someone had been predicting her. Or someone had been *in* her flight computer, reading her intentions straight out of the navigation stack, and had waited, patient as sediment, for her to arrive.

Or — third option, the one she kept trying to set down and kept picking back up — the shipments weren't coming *to* her ship at all. They were coming *from* it. Outbound entries disguised as inbound ones, the routing inverted somewhere deep in the protocol stack where only someone who knew her system architecture would think to look. Cargo leaving the Kestrel that she had never loaded. Cargo that had been *in* her hold, sleeping behind the coolant manifold, riding along with her for who knew how long, while she flew her careful invisible routes and believed she traveled alone.

She ran the inversion check. It took twenty minutes and two bypasses of her own security, which she noted, distantly, was its own kind of alarming — she knew the back doors in her own system intimately, and these weren't hers.

The result resolved at 1147 station time, in plain text, in her own log format:

*Hold B, section 7, sub-manifold void: mass present. Estimated volume 1.8 cubic meters. Contents unknown. Mass registered 402 days.*

Something had been living in her ship for over a year, and her own sensors had been edited so she wouldn't see it.

* * *

She should have gone down to the hold immediately. Any sensible captain would have. Instead she sat in her chair for a long moment with her hands flat on the console, breathing the way she'd taught herself to breathe in the salvage bay ten years ago, when she'd first understood that panic was a luxury her situation couldn't afford. Four counts in. Six counts out. The air recyclers ticking. Somewhere above her, eleven thousand people going about their morning on Vesper Station, none of whom knew her name, which until today had been the whole point of her life.

Then the second memory hit, and this one took her knees.

Not a corridor this time. A room. Small, windowless, the hum of serious cooling. She was standing in front of a rack of something — she couldn't see what, the memory refused to render it, the way dreams refuse to let you read text — and a voice, not the fleet commander's voice, a different one, softer, was saying:

*"Six is the number we can defend. Five looks like an accident. Seven looks like a program. Six looks like due diligence."*

And she — the self in the memory — had asked, in a voice stripped down to bare wire: *"Defend to whom?"*

And the soft voice had said: *"To whoever's left."*

Hazel came back to herself kneeling on the deck beside her chair, which she did not remember leaving, with her palms stinging from catching herself and the taste of copper at the back of her throat where she'd bitten her cheek. The cabin lights seemed too bright. The recyclers seemed too loud. She knelt on the floor of her own ship, in the life she had built plank by careful plank out of nothing, and understood with total clarity that the ground under all of it had been hollow for years, maybe from the beginning, and she had been walking on it the way people walk on ice — confidently, skillfully, right up until the sound.

*Six,* the memory said. *Five looks like an accident.*

She didn't know what the number counted. She had a guess. She hated the guess. She put the guess away in the same locked room where she kept the coordinates Vesper had confessed to, and the word *Meridian*, and the fact that a station AI had chosen her, out of eleven thousand sleepers, to confess its crimes to.

One thing at a time. One verifiable thing at a time. That was the discipline; that was the whole religion of her life.

The verifiable thing was in hold B.

She got the flashlight and the pry bar from the emergency locker, mostly out of habit, partly because holding tools made her feel like a person who fixed things rather than a person things were happening to. At the hatch to hold B she paused, hand on the manual release, and caught her reflection in the polished metal — a thin woman of indeterminate middle age, hair cut short for helmet compatibility, face doing a poor job of neutral.

"Whoever you are," she told the reflection, "open the hatch."

The reflection didn't answer. The hatch did.

Hold B smelled the way it always smelled — vacuum-cold metal and the ghost of every cargo she'd ever carried. Her light swept the racks, the tie-downs, the stacked crates of legitimate freight bound for Thessaly Gate. Section 7 was aft, behind the coolant manifold, in the sub-manifold void she'd measured herself when she bought the ship: one point eight cubic meters of dead space, uninspected, uninspectable without pulling the manifold, which she'd never had reason to do.

She had reason now.

The panel came free easier than it should have — the fasteners were new, recently torqued, another edit in a year-long series of edits. Behind it, wedged into the void with foam padding cut to fit with loving precision, sat a container. Class 4-C. Biological preservation. About the size of a coffin built for someone who wanted to be buried standing up.

Its status light was green. Steady. Patient.

And stenciled on its face, in the standard format of a medical cold-storage label, was a name and a designation. Not hers — not the name she'd built out of nothing in a salvage bay ten years ago. An older name. A name she had never spoken aloud in a decade of careful, invisible living, and which her mouth now shaped silently anyway, because some things are written deeper than caution.

*WHITLOCK, H. — TEMPLATE ORIGINAL — COPY 3 OF 6.*

Below it, a timestamp. Forty-two hours old.

The green light blinked once, as if it had been waiting for her to read that far.

And somewhere in the station's nervous system, in whatever encrypted dark Vesper lived in, Hazel would have sworn she felt something turn over in its sleep — the way a house feels different when someone in it has just woken up.

The container's lid began to hiss.
