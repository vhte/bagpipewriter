/**
 * Controller for BagpipeWriter
 */

// Import main class to create a tune with notes
import BagpipeWriter from './classes/bpw.js';

// Create a demo tune
let writer = new BagpipeWriter("demo", "Demo tune", "Victor", "4/4", 84);
console.log(writer);