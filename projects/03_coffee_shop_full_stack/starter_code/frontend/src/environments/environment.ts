/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'jg23-dev.us', // the auth0 domain prefix
    audience: 'coffee', // the audience set for the auth0 app
    clientId: '7I4Y4XD0bywao22y8NjX2WZ6k0b2LA9M', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application. 
  }
};
