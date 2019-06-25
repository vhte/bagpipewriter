/** Note class */
class Note {
	constructor(name, time) {
		const LowA = "LA";
		const LowG = "LG";
		const B = "B";
		const C = "C";
		const D = "D";
		const E = "E";
		const F = "G";
		const HighG = "HG";
		const HighA = "HA";
		const allNotes = [LowA, LowG, B, C, D, E, F, HighG, HighA];
		
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