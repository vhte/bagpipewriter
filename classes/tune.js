/**
 * Tune class with the piece properties
 */
export class Tune {
	constructor(name, time, author) {
		this.name = name;
		this.time = time; // 3/4
		this.author = author;
	}
	
	getTime() {
		return this.time;
	}
	setTime(value) {
		this.time = value;
	}
	
	getName() {
		return this.name;
	}
	setName(value) {
		this.name = value;
	}
	
	getAuthor() {
		return this.author;
	}
	setAuthor(value) {
		this.author = value;
	}
	
	addNote(note) {
		this.addNotes([note]);
		return this;
	}
	
	addNotes(notesSet) {
		return this;
	}
}