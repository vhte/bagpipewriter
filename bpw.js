/** Class of BagpipeWriter representing the object that will manage Bagpipe Player symbols (using jsdoc)
 * This class works as a controller */
const ROOT = "http://localhost/bagpipewriter/";
const CLASSDIR = ROOT + "classes/";

import { Note } from "./classes/note.js";
import { Tune } from "./classes/tune.js";

class BagpipeWriter {
	/**
	 * Set the file to manage
	 * @param {string} file Name of the file to create/update
	 */
	constructor(file) {
		this.file = file + ".bww";
		this.tune = new Tune("Name", "6/8", 60);
	}
}