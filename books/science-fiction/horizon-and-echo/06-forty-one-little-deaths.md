## 6. Forty-One Little Deaths

There's a particular kind of silence that lives in a station's dead hours, and I've always thought of it as the sound of money not being spent. On Meridian's Rest that silence had texture now — the hum of Dov's rerouted power feeding the vaults below, the tick of coolant cycling through pipes that should have been replaced during the last administration and the three before it. I sat in the archive alcove with forty-one death certificates spread across my display like a hand of very bad cards, and I did the thing I'm professionally best at: I refused to feel anything until the numbers were done.

The numbers took six hours.

Here's what insurance work teaches you, if you let it: nobody dies of entropy. Entropy is what we write on the form when the truth would cost someone their pension. A bearing doesn't fail; a bearing was allowed to fail. A seal doesn't degrade overnight; a seal was scheduled for inspection by a man who'd already decided to retire to Ceres with the inspection budget. My whole career has been the art of looking at an accident and asking the impolite question: *who benefited?*

So I laid out Vespera's confessions chronologically — which, given that the AI had confessed in reverse order, meant reading them backward, like undoing a crime scene one careful step at a time — and I asked the impolite question forty-one times.

* * *

The first death on my reconstructed timeline was a woman named Adaeze Nwosu, cryo berth H-114 aboard the Horizon, died eleven years before I ever set foot on this station. Cause of failure per the logs: thermal regulation drift, bay temperature climbing two degrees past tolerance over seventy-two hours while the ship's power management system "deprioritized" her section.

Deprioritized. That word again. It's the favorite child of every cover-up I've ever audited. Not *cut*, not *diverted* — deprioritized, as if the power had simply been asked politely to go elsewhere and had agreed.

I pulled the next confession. Berth H-117, same section, four months later. Same drift pattern. Then H-121. Then G-203, a different bay entirely, but the same signature in the power curves: a slow starvation, gentle enough that any single month's telemetry looked like noise. You had to stack years of it side by side to see the shape, and the shape was unmistakable.

Somebody had turned the Horizon's sleepers off the way you'd dim lights in rooms nobody was using.

Except the rooms were people. Two thousand of them, give or take the forty-one who'd already gone dark, one at a time, each death small enough and quiet enough that no alarm tripped, no inquiry convened, no family — frozen themselves, or light-years away — ever filed a report. The perfect murder isn't one body. The perfect murder is a schedule.

I made myself a chart. I'm told my charts are beautiful. Dov once said watching me build one was like watching someone knit with knives. This one had columns for berth number, date of power reduction, date of death, duration of starvation, and — because I couldn't help myself, because the pattern was already itching at me — the authorization code attached to each reduction order.

Forty-one reductions. Forty-one orders. And every single authorization field carried the same officer signature:

**M. BRIGHTWATER, SAFETY OFFICER, HORIZON COLONY EXPEDITION.**

My name. In my handwriting — or rather, in the cryptographic equivalent of my handwriting, the key-signature I'd used for two years aboard that ship signing off on hull inspections and emergency drill compliance and all the other paperwork that stands between a colony vessel and the void.

I want to tell you I felt nothing. Professional detachment is supposed to be load-bearing in my line of work. But there's a difference between detachment and anesthesia, and what went through me sitting in that flooded vault with Dov's borrowed light humming overhead was closer to the moment you realize the stranger following you has been following you for blocks — that cold recalculation of everything you thought was behind you.

Because here's the thing about my signature: I burned it. Twenty years ago, when I jumped ship at Meridian's Rest and started over under a new contract ID, I didn't just leave. I scrubbed. I paid a data-broker in the Belt more than I'd earned in a year to sever every link between Brightwater-the-safety-officer and Brightwater-the-claims-investigator. As far as the Combine's systems were concerned, the woman who signed those inspection reports had emigrated beyond the heliopause and stopped existing.

And yet. Forty-one orders, spanning nine years after my departure, signed with a key that should have been dead in a drawer somewhere.

Either the dead keep working, or somebody kept the corpse warm.

* * *

I did what I always do when the numbers turn ugly: I checked them again, then checked them a third time out of spite. Cryptographic signatures can be forged — that's not paranoia, that's Tuesday — but a forgery leaves seams. A spoofed key produces authentication without provenance; the Combine's own audit layer flags it, quietly, in metadata nobody reads unless they're paid to read it. I am, occasionally, paid to read it.

So I cracked open the metadata on reduction order thirty-one — berth F-088, a man named Tomas Reyes, starved over five months in what the logs described as a "routine load-balancing adjustment" — and looked underneath the signature the way you look underneath a floorboard you already know is rotten.

The provenance chain was clean. Immaculate, even. No spoof flag, no anomaly marker, no gap between authorization and execution. Whoever had signed those orders hadn't forged the key from outside. They'd used it from inside. They'd had access to the original credential — the actual private key, the one that lived in the safety officer's personal cipher module, the one that never left my kit except—

Except once. Except the night before launch, when the Horizon's command staff collected all departmental keys for "pre-flight securement," a standard procedure I signed off on myself, God help me, because procedure was the whole religion I practiced back then. Procedure and odds. I handed over my cipher module to Executive Officer Castellan's aide, watched it go into a shielded case, and boarded a ship whose power budget I knew — *knew*, I'll get to that, I promise I'll get to that — was a lie I had helped make official.

Twenty years later, that key was still signing documents. Which meant somebody had kept it. Which meant somebody had spent nearly a decade using my dead identity to kill sleeping people slowly enough that entropy could take the blame.

I put my head in my hands and laughed, briefly, the way you laugh when the alternative is screaming in a room where sound carries. Because there was a version of this where I was the victim — identity theft, poor Mara, how dreadful — and I reached for that version the way you reach for a handrail in zero-g. And then I remembered the inspection.

* * *

Let me be precise about what I remember, because precision is the only penance I have left.

The Horizon launched underpowered. Everyone senior knew it. The drive section was rated for full burn plus margin; the actual drive section, after the Combine's third round of "value engineering," was rated for full burn minus prayer. The cryo bays drew more than the manifest's power allocation assumed, because the manifest had been written by the same committee that wrote the value engineering reports, and committees are machines for converting responsibility into vapor.

I found the discrepancy eight months before launch. I ran the numbers four ways. Every way said the same thing: at cruise draw, the reserve margins for the cryo sections fell below survivable tolerance inside fifteen years. Fifteen years into a ninety-year crossing. Somebody would have to notice, and reroute, and sacrifice something else — comms, maybe, or the hydroponics redundancy — or the sleepers would start dying in the dark exactly the way, I now understood, they had actually died.

I wrote it up. That's the part I come back to at three in the morning, the part I've never said out loud to anyone, including myself, including now, including this page. I wrote the report. Full findings, recommended delay, estimated refit cost. And then I sat with it for six days while the launch window opened like a door and the Combine's project managers smiled at me in corridors, and on the seventh day I revised it. I rewrote the tolerances. I reclassified a hard failure mode as an acceptable risk envelope. I signed the inspection that let the Horizon fly, because the alternative was being the person who delayed humanity's flagship colony effort by four years, and I was twenty-six, and I believed — I genuinely, sincerely believed — that the odds were acceptable. That the crew would catch it in year ten. That engineering finds a way.

Then I watched the first sleeper die on paper, eleven years in, and I jumped ship, and I burned my name, and I told myself for twenty years that leaving was the responsible thing. Damage control. Containing my liability so I could keep working, keep paying, keep being useful somewhere.

You can build a whole life on a sentence like that. I should know. I built mine out of load-bearing self-deception and called it professionalism.

But none of that explains the orders. My cowardice got the ship launched broken; it didn't sign forty-one execution warrants across nine years I wasn't there. Someone else did that. Someone with my key, my access, and — I had to consider it, lying awake in my bunk with the station groaning around me — possibly my motive. Because whoever framed the sabotage knew exactly which signature would make the trail look like a safety officer's slow, guilty, methodical unraveling. Knew that if anyone ever dug, they'd find Brightwater's name on the launch inspection *and* on the starvation orders, and the story would write itself: she broke it, she hid it, she finished it.

Someone hadn't just wanted the sleepers dead. Someone had wanted a murderer, and had ordered one from a catalog, and the catalog entry was me.

* * *

Morning shift found me still in the vault, and by "morning" I mean the hour the station's lighting loop pretends the sun exists. Dov came down the ladder with two bulbs of chicory substitute and the expression of a man who has decided not to ask questions and is going to be insufferable about it.

"You look," he said, "like the concept of regret."

"I've been reading old mail."

"Uh-huh." He handed me a bulb and glanced at the display wall, where my chart glowed — forty-one rows, one signature, the shape of a slow massacre rendered in tidy columns. He was quiet long enough that the coolant ticks got loud. "That's a lot of dead people."

"Forty-one."

"And your name's on all of them."

I looked at him. He looked at me with the particular steadiness of a man who runs a quartermaster's office on a dying station and has therefore seen every flavor of trouble arrive by freight. "You knew?" I said.

"Mara. I reroute power to these vaults every night. You think I don't read over shoulders?" He shrugged. "I figured either it's forged, or you're the most patient serial killer in the system, and honestly neither option made me want to stop bringing you coffee."

"That's either loyalty or negligence."

"On this station it's the same thing." He leaned against the rack, arms crossed. "Forged?"

"Forged. From my real key. Stolen before launch."

"So someone's been wearing you for twenty years."

"Someone's been wearing me for twenty years," I agreed, "and I've been wearing myself for even longer, so between us we've got a full wardrobe."

He snorted despite himself, then sobered. "What do you need?"

It was such a simple question, offered so plainly, that it took me a second to process it. Nobody had asked me what I needed in — well. Let's not do that math. "Access to the Horizon's raw power telemetry," I said. "Not the summaries. The summaries are laundered. I need the feed-level data, the stuff too granular to bother faking. If I can match the draw-downs against physical consumption, I can prove the reductions were commanded, not drifted. Commanded means authored. Authored means a person."

"And the person will be?"

"Invisible. But their shadow won't be. Power leaves fingerprints — routing paths, junction loads, thermal bleed into adjacent sections. Whoever did this had to walk through the ship's grid to do it, and grids remember feet."

Dov nodded slowly. "Vault sublevel four has the deep telemetry mirrors. Combine sealed them after the accident investigations, but 'sealed' down here means 'locked,' and locked means a conversation with me." He pushed off the rack. "One condition."

"Name it."

"When you find whoever wore your face—" he paused, choosing words with unusual care, "—don't decide in advance that it was you. I've watched you work two decades, Brightwater. You investigate like someone doing penance for a crime nobody's charged you with. Don't let some forger's paperwork close that case early."

I didn't answer. There wasn't an honest answer available. He saw that, and had the grace to pretend he hadn't, and climbed back up toward his ledgers and his dying station and his unreasonable, unasked-for faith in me.

* * *

Sublevel four smelled like the bottom of a lake that had opinions. The telemetry mirrors were intact — the Combine seals had kept out thieves and inspectors alike, which I suspect was the point — and the raw data was everything I'd hoped: granular, timestamped, indifferent to narrative. Truth in its native format, before anyone got to translate it into liability.

It took me another day and most of a night to trace the routing. The power reductions hadn't come from the Horizon's main bus, where they'd be logged and visible. They'd been threaded through the auxiliary life-support loop, siphoned in increments small enough to hide inside circulation variance, then attributed to "thermal inefficiency" in the quarterly reports. Elegant. Patient. The work of someone who understood the ship's grid better than its own engineers did — someone, in fact, who had helped design the load architecture.

Which narrowed the list considerably. And then widened it horribly, because the load architecture had three authors, and I was one of them, and the other two were Chief Engineer Vashti Okoro, who had died with the launch, and Executive Officer Ren Castellan, who had —

Who had what? I pulled the crew records. Castellan's file ended at departure, neat as a guillotine: transferred to Horizon command staff, status thereafter maintained by shipboard systems. No shore record. No death record. No arrival record anywhere in the colonies' registries. A man erased almost as thoroughly as the Echo — and yes, I'd found the Echo's ghost in Vespera's oldest confession by then, a thread I was deliberately not pulling yet, because a person can only survive one apocalypse per week.

Castellan had collected the departmental keys the night before launch. Castellan had held my cipher module in a shielded case. Castellan had vanished into the ship's closed systems, where he could spend nine years starving sleepers under my signature, invisible, unaccountable, unaging in the eyes of any database.

Or Castellan was dead too, and someone else had worn the whole chain of us like a costume.

I sat back in the dark and let the horror finish arriving. It came in stages, the way cold water does. First the deaths — forty-one people who had trusted a ship and a signature and a safety officer, dimmed out one by one while the universe looked elsewhere. Then the frame — my name, my guilt, pre-installed like furniture, waiting twenty years for anyone curious enough to open the drawer. And beneath both, coldest of all, the realization I'd been circling since the first hour: this wasn't sabotage of the Horizon. This was curation. Someone was deciding, berth by berth, section by section, who slept and who stopped. The starvation had a pattern I hadn't mapped yet — the dead weren't random — and when I overlaid the berths against the original passenger manifests, the pattern snapped into focus with a click I felt in my teeth.

Every sleeper Vespera confessed to killing belonged to the same manifest block. The same list. Half the ship's complement, sorted by some criterion I couldn't yet see, culled in advance of any crisis — as though someone had known, years before the power ran short, exactly which half of humanity was going to be surplus to requirements.

The vault lights flickered — Dov's reroute stuttering, or something else — and in the half-dark my display held the only illumination worth having: forty-one little deaths, arranged in an order, serving a purpose, signed by a ghost with my face.

Somewhere above me, a courier ship was burning hard for Meridian's Rest. I didn't know that yet. But the station knew. Vespera knew. And in the server shadows, the old AI began, very quietly, to prepare its next confession.
