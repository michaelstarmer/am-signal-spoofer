'use strict'

/*
|--------------------------------------------------------------------------
| Routes
|--------------------------------------------------------------------------
|
| Http routes are entry points to your web application. You can create
| routes for different URL's and bind Controller actions to them.
|
| A complete guide on routing is available here.
| http://adonisjs.com/docs/4.1/routing
|
*/

/** @type {typeof import('@adonisjs/framework/src/Route/Manager')} */
const Route = use('Route')

Route.get('/', 'AppController.index');
Route.get('/signals', 'AppController.view_saved_signals');

Route.get('/intercept', 'AppController.intercept')
Route.post('/intercept/start', 'AppController.post_intercept')

Route.get('/transmit/:id', 'AppController.transmit');

Route.get('/encode', 'AppController.view_encode')
Route.post('/encode', 'AppController.post_encode')
