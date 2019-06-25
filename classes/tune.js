/**
 * Tune class with the piece properties
 */
import Note from './tune.js';

class Tune {
	constructor(name, tempo, author) {
		this.name = name;
		this.tempo = tempo;
		this.author = author;
	}
	
	getTempo() {
		return this.tempo;
	}
	setTempo(value) {
		this.tempo = value;
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