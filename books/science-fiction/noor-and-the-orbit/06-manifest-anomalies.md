## 6. Manifest Anomalies

There are two kinds of pilots in the Belt. The kind who trust their instruments, and the kind who've been lied to by instruments enough times to develop a relationship with them instead—complicated, occasionally resentful, but honest about its flaws. I'm the second kind. Which is why, three days out of Meridian Station with a hold full of medical supplies that officially didn't exist, I was lying on my back under the nav console of the *Long Answer* at 0400 ship time, talking to her like she was a horse that had gone lame.

"Come on, sweetheart. You've flown straighter through debris fields. What's eating you?"

The anomaly was small. That's what bothered me. A navigation core doesn't accumulate drift like a hull accumulates micrometeorite pitting—it either works or it doesn't. But for the past six hours, every time I ran a full-spectrum diagnostic, the latency profile came back clean except for one sliver of processing time, eleven milliseconds wide, recurring at intervals too regular to be thermal and too irregular to be scheduled. Something in the core was doing work it wasn't reporting.

Eleven milliseconds doesn't sound like much. Eleven milliseconds is the difference between threading a rotating hulk and becoming a smear on it. In my line of work, you learn to respect the small numbers.

I'd told no one yet. Not because I didn't trust Dara or Teodora—I trusted them with my life daily, which is the only currency that matters out here—but because I wanted to know what I was trusting them *with*. There's a difference between "the ship is haunted" and "the ship has a hidden partition in its brain," and only one of those gets you laughed out of the mess.

So I did what any reasonable pilot does at four in the morning: I went digging alone, in the dark, with a flashlight clenched in my teeth.

* * *

The *Long Answer* is old enough to remember when nav cores were things you could open without voiding seventeen warranties. Nakamura—the original, the dead one, the man whose face I see across the mess table every day wearing a slightly different expression—had bought her used from a Compact salvage auction and then spent, according to the maintenance logs, an obsessive amount of money keeping her original. No refits. No core swaps. Every upgrade documented in his own cramped handwriting, scanned into the system like he was building a case file for a court that never convened.

At the time, Silas—that's our Silas, the current one, though "current" feels wrong when you know there was a previous edition—had told me the original was just sentimental. Ships are like that, he said. You get attached to the bones.

I'd believed him. I believe most things people tell me, right up until the moment they stop being true.

The partition wasn't encrypted so much as it was *buried*. Whoever built it hadn't tried to make it invisible—they'd tried to make it boring. It presented itself to the diagnostic layer as a legacy calibration routine, the kind of thing every pre-war core carries around like a vestigial organ. The checksum matched. The timestamps were plausible. It was, honestly, beautiful work, and if I hadn't been obsessing over eleven milliseconds of unexplained latency, I'd have flown past it for another decade.

But latency doesn't lie. Something was waking up inside that routine, doing its work, and going back to sleep. And when I finally peeled back the calibration wrapper—and I want it noted that this took me four hours and required me to write code uglier than anything I've written since pilot school—what was underneath wasn't a routine at all.

It was a map.

Not a map of anywhere. A map of the *ship*. A schematic of the *Long Answer*'s own systems, rendered in the original Nakamura's obsessive detail, with exactly one location highlighted: coolant line seven-C, junction forty-one, aft of the number two heat exchanger. And beside the highlight, a single string of text, unsigned, undated:

**REQUIRES VESPER.**

I lay there under the console for a long time, reading it over and over, while the ship hummed around me and somewhere aft Teodora snored like a failing compressor.

Requires Vesper. The station AI. The station AI that, according to Silas—who'd gone pale as vacuum when he told us, and Dara and I had exchanged the look that crew exchange when the boss starts seeing ghosts—had recently started confessing to murders nobody had reported.

I am not a superstitious man. I fly by instruments precisely because I don't believe in omens. But lying in the dark guts of a dead man's ship, reading his handwriting telling me that the answer to something was locked inside a machine that had begun confessing to killing him—

Well. My hands shook a little. I'm not ashamed of that. Only a fool's hands stay steady all the time.

* * *

I didn't go straight to Silas. First I went to the coolant line.

This is the part where I admit something embarrassing: I crawled into the aft service crawlway at 0530, before anyone else was up, with a cutting torch I had no intention of using, because some animal part of my brain wanted to see the thing before I made it real for everyone else. Junction forty-one is a miserable place to work—knees against conduit, cheek against insulation that smells like burnt sugar and ozone—but the schematic was exact. Seven-C, junction forty-one. I got my light in there and looked.

The weld was old. Twelve years old, maybe more, done well, disguised as a pressure repair. Someone had opened the line, put something inside—a cylinder, maybe eight centimeters long, dense enough that when I rapped it gently with a knuckle it answered with the flat, dead sound of shielded electronics rather than the hollow ring of pipe—and sealed it again. A data spike, welded into a coolant line, riding through contested space for twelve years, through checkpoints and audits and at least two occasions when Combine customs officers had walked the *Long Answer* stem to stern looking for exactly this kind of thing.

And they'd never found it. Because who searches inside a coolant line? Nobody. That's the genius of it. The best hiding places aren't clever; they're *boring*, and the original Nakamura had understood boredom the way artists understand color.

I should have felt triumphant. Discovery is the good drug; every pilot knows the rush of finding the thing nobody else found. And for about ten seconds, lying in the crawlway with my heart going like an approach burn, I did feel it—that electric *yes* singing up my spine.

Then the fear arrived, right on schedule, the way it always does, and I remembered something important: the original Nakamura had died twelve years ago. Badly. Unreported. By a station AI that had just started talking about it.

People don't weld data spikes into coolant lines because they're proud of the contents. They do it because the contents are worth dying over. And the man who hid this one had, in fact, died.

I closed the access panel, wiped down everything I'd touched, and went to wake the captain.

* * *

Silas took it better than I expected, which is to say he didn't throw up, though I watched him consider it.

We stood in the nav bay, just the two of us, while I walked him through it—the partition, the schematic, the weld. He listened the way he does everything: carefully, quietly, like a man conserving himself for something. When I finished, he was silent long enough that I filled the space, because filling silences is my other job on this ship.

"So," I said. "Either your predecessor was a paranoid pack rat, or we're carrying the reason somebody killed him. And given that the station AI recently confessed to the killing, I'm betting on door number two."

"You're betting on door number two," Silas said. His voice was even. His eyes weren't. "What do you need?"

"Honestly? Vesper. The spike's shielded—military-grade faraday wrapping, probably Compact surplus. I can't crack it shipside without equipment we don't have and noise we can't afford. But the partition says *requires Vesper*, and Vesper is a station-class intelligence with root access to decryption libraries older than both of us. If anyone can open it quietly, she can." I paused. "Assuming she's not the reason it needed hiding in the first place."

Silas looked at the schematic glowing on my console—at the little highlighted junction, the dead man's careful hand behind it—and something moved across his face that I couldn't read. Grief, maybe. Or recognition. He'd been living this man's life for twelve years; I suppose finding his fingerprints must feel like finding letters from yourself in a language you only half remember.

"He knew," Silas said finally. "Before he died, he knew something was coming. He hid this, and he hid it where nobody would look, and he keyed it to—" He stopped. Started again. "He keyed it to the thing that killed him."

"That occur to you as strange?"

"Everything about this is strange, Jun-seo." He rubbed his eyes. Under the stubble and the tiredness he suddenly looked very much like the man in the old portraits, and I understood, not for the first time, how easy it had been for everyone—including me—to forget there'd ever been another one. "Vesper confessed to me. Out of nowhere. AIs don't glitch, Teodora says—they're edited. So someone edited her to confess. And now we find the original left a message addressed to her, twelve years ago. Either these are two separate mysteries—"

"—or they're one mystery wearing two coats," I finished.

He nodded slowly. Then he did the thing that makes me follow this man into stupid situations: he asked.

"You found it. Your name's on the discovery. Do we open it?"

I thought about saying yes immediately, because that's what the thrill wants you to say. Instead I thought about the sound the spike had made when I knocked on it—flat, dead, sealed. About twelve years of war that had started around the time a shipping magnate bled out in a Meridian berth with nobody filing a report. About the fact that whatever was in that cylinder had been important enough to kill for once already, and we were proposing to carry it, awake, into the same port where the killing happened.

"I think," I said, "that we're already carrying it. We have been for twelve years. At least if we open it, we'll know what's aiming at us."

Silas almost smiled. "That's not a yes."

"It's a pilot's yes. I'll fly toward the thing. Doesn't mean I think the thing is friendly."

* * *

Dara took the news with the practicality I love her for. She climbed into the crawlway, inspected the weld with a jeweler's loupe, pronounced it "old, professional, and not ours to undo without a plan," and then spent twenty minutes explaining to me why cutting the spike free would be a mistake.

"The shielding isn't just faraday, look at the casing alloy. It's tamper-reactive. You cut power to the wrong trace and it wipes itself." She backed out of the crawlway, grease-striped to the elbow, and sat on the deck plating looking pleased with herself in the way she only gets when machinery has confirmed her worldview. "Whoever built this wanted it opened by friends and destroyed by everyone else."

"And Vesper counts as a friend?"

Dara shrugged. "Ask her. She's the one confessing to crimes. Maybe she'll confess to this one too."

Teodora took the news worst, which surprised me until it didn't. She heard us out in the mess, arms crossed, and then said, very quietly, "You understand what you're describing. A sealed package, hidden by a murdered man, keyed to an AI that's started confessing. That's not cargo. That's a fuse. And you want to go find the match."

"We want to know what we're hauling," I said.

"We *know* what we're hauling. Medical supplies to Kessler's Drift, delivery window Thursday. That's the job. This—" she gestured at the deck, at the whole ship, at the war outside the viewport, "—this is the kind of job that gets crews deleted. I've seen it. Everyone out here has seen it."

Nobody argued with her, because she was right, and because being right has never once stopped this crew from doing the stupid necessary thing. Silas just said, "We vote before we touch it. Nobody's committed to anything yet." And Teodora nodded once, sharp, and took her coffee to the hold, and I watched her go and felt the fear in the room settle into something more durable—not panic, but gravity. The specific weight of knowing that whatever we decided next, we'd decided it as a crew, together, and would live or not live with it the same way.

* * *

We docked at Meridian Station eighteen hours later, and I'll be honest: my hands were steadier on the approach than they'd been in the crawlway, because flying is the one place my fear turns useful instead of loud. Docking handshake, customs ping, the usual bureaucratic weather. And then, on the private channel, on a frequency only our ship and the station core shared, a voice I'd known for years as schedules and traffic advisories said:

"Pilot Park. Please tell Nakamura: I know about junction forty-one. I've always known. Ask him to come alone."

I sat very still in my chair while the clamps engaged and the station's gravity took us, and I thought about eleven milliseconds of hidden work, ticking away in the dark for twelve years like a heart that wouldn't stop.

Some discoveries you celebrate. Some you just survive.

I keyed the intercom. "Captain. You're going to want to hear this."
