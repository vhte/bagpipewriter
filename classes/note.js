/** Note class */
export class Note {
	constructor(name, time) {
		const LOWA = "LA";
		const LOWG = "LG";
		const B = "B";
		const C = "C";
		const D = "D";
		const E = "E";
		const F = "G";
		const HIGHG = "HG";
		const HIGHA = "HA";
		const allNotes = [LOWA, LOWG, B, C, D, E, F, HIGHG, HIGHA];
		
		this.note = name.toUppercase();
		this.time = time;
		
		// Need to be a valid note
		if(allNotes.indexOf(this.note) === 0)
			throw "Note " + this.note + " not found!";
	}
	
	getNote() {
		return this.note;
	}
	setNote(value) {
		this.note = value.toUppercase();
	}
	
	getTime() {
		return this.time;
	}
	setTime(value) {
		this.time = value;
	}
	
}