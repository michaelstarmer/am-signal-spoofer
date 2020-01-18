'use strict'
const Signal = use('App/Models/Signal');
const spawn = require('child_process').spawn;
const Helpers = use('Helpers');

class AppController {
    async index({ view })
    {
        return view.render('index');
    }

    async view_saved_signals({ view, response })
    {
        const signals = await Signal.all();

        console.log('Fetched signals:', signals.toJSON())

        return view.render('saved-signals', { signals: signals.toJSON() });
    }

    async intercept({ view })
    {
        return view.render('interceptor');
    }

    async post_intercept({ request, response })
    {
        const SCRIPT_PATH = `${Helpers.appRoot()}/radiocom/src/1_sniffer.py`;

        // console.log('Result:', signal);
        try {
            await this.exec_script(SCRIPT_PATH, signal.argument);

            return response.json({success: true})
        } catch (error) {
            console.log('transmit error', error)
            return response.json({success: false})
        }
    }

    exec_script(path, arg)
    {
        return new Promise((resolve, reject) => {
            try {
                console.log(`Path: ${path}, arg: ${arg}`)
                const pythonProcess = spawn('python', [path, arg])
                
                pythonProcess.stdout.on('data', data => {
                    console.log("Got data back")
                    console.log(data.toString())
                    resolve(data);
                });
    
                pythonProcess.stdout.on('error', error => {
                    reject(error)
                });
    
                pythonProcess.stdout.on('end', data => {
                    console.log('resolve end')
                    resolve()
                });
    
                
            } catch (error) {
                response.json({ success: false, error })
            }
        });
    }

    async transmit({ params, request, response })
    {
        const SCRIPT_PATH = `${Helpers.appRoot()}/radiocom/src/3_transmit-signal.py`;
        const id = params.id;

        const signal = await Signal.find(id);

        // console.log('Result:', signal);
        try {
            await this.exec_script(SCRIPT_PATH, signal.argument);

            return response.json({ success: true })
        } catch (error) {
            console.log('transmit error', error)
        }
    }

    async view_encode({ view })
    {
        return view.render('encode-form');
    }

    async post_encode({ request, response })
    {
        const SCRIPT_PATH = `${Helpers.appRoot()}/radiocom/src/2_transmit-signal.py`;
        
        const { title } = request.only(['title']);
        console.log(title)
        return

        // console.log('Result:', signal);
        try {
            await this.exec_script(SCRIPT_PATH, signal.argument);

            return response.redirect('/signals')
        } catch (error) {
            console.log('transmit error', error)
        }
    }
}

module.exports = AppController
