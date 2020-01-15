'use strict'

class AppController {
    async index({ view })
    {
        return view.render('index');
    }
}

module.exports = AppController
