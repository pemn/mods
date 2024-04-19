using System;
using System.Collections.Generic;
using Verse;

namespace RimWorld
{
	internal class Recipe_Rejuvenate : Recipe_Surgery
	{
		public override void ApplyOnPawn(Pawn pawn, BodyPartRecord part, Pawn billDoer, List<Thing> ingredients, Bill bill)
		{
			if (base.CheckSurgeryFail(billDoer, pawn, ingredients, part, bill))
			{
				pawn.ageTracker.AgeBiologicalTicks = (long) (pawn.ageTracker.AgeBiologicalTicks * 1.2);
			} else {
				pawn.ageTracker.AgeBiologicalTicks = (long) (pawn.ageTracker.AgeBiologicalTicks * 0.9);
			}
		}
	}
}
