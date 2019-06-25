/** Class of BagpipeWriter representing the object that will manage Bagpipe Player symbols (using jsdoc)
 * This class works as a controller */
import Tune from './tune.js';
class BagpipeWriter {
	/**
	 * Set the file to manage
	 * @param {string} file Name of the file to create/update
	 */
	constructor(file) {
		this.file = file + ".bww";
	}
}