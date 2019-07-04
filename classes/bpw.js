/** Class of BagpipeWriter representing the object that will manage Bagpipe Player symbols (using jsdoc) */
const ROOT = "http://localhost/bagpipewriter/";
const CLASSDIR = ROOT + "classes/";

import { Note } from "./note.js";
import { Tune } from "./tune.js";

export default class BagpipeWriter {
	/**
	 * Set the file to manage
	 * @param {string} file Name of the file to create/update
	 */
	constructor(file, tuneName, author, time, tempo) {
		this.file = file + ".bww";
		this.author = author;
		this.tempo = tempo;
		this.tune = new Tune(tuneName, time, author);
	}
}