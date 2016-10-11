/**
 * FirebaseUI initialization to be used in a Single Page application context.
 */
// FirebaseUI config.
var uiConfig = {
  'callbacks': {
    // Called when the user has been successfully signed in.
    'signInSuccess': function(user, credential, redirectUrl) {
      handleSignedInUser(user);
      // Do not redirect.
      return false;
    }
  },
  // Opens IDP Providers sign-in flow in a popup.
  'signInFlow': 'popup',
  'signInOptions': [
    // TODO(developer): Remove the providers you don't need for your app.
    {
      provider: firebase.auth.GoogleAuthProvider.PROVIDER_ID,
      scopes: ['https://www.googleapis.com/auth/plus.login']
    },
    {
      provider: firebase.auth.FacebookAuthProvider.PROVIDER_ID,
      scopes :[
        'public_profile',
        'email',
      ]
    },
    firebase.auth.EmailAuthProvider.PROVIDER_ID
  ],
  // Terms of service url.
  'tosUrl': 'https://www.google.com'
};

// Initialize the FirebaseUI Widget using Firebase.
var ui = new firebaseui.auth.AuthUI(firebase.auth());
// Keep track of the currently signed in user.
var currentUid = null;

var database = firebase.database();

var template_moustache = null;
$.get('status.stache.html', function(templates) {
// Fetch the <script /> block from the loaded external
// template file which contains our greetings template.
template_moustache = $(templates).filter('#tpl-files').html();});


/**
 * Redirects to the FirebaseUI widget.
 */
var signInWithRedirect = function() {
  window.location.assign('/widget');
};


/**
 * Open a popup with the FirebaseUI widget.
 */
var signInWithPopup = function() {
  window.open('/widget', 'Sign In', 'width=985,height=735');
};


/**
 * Displays the UI for a signed in user.
 */

var handleSignedInUser = function(user) {
  currentUid = user.uid;
  document.getElementById('user-signed-in').style.display = 'block';
  document.getElementById('user-signed-out').style.display = 'none';
  document.getElementById('name').textContent = user.displayName;
  document.getElementById('email').textContent = user.email;
  document.getElementById('uid').textContent = user.uid;
  if (user.photoURL){
    document.getElementById('photo').src = user.photoURL;
    document.getElementById('photo').style.display = 'block';
  } else {
    document.getElementById('photo').style.display = 'none';
  }

  document.getElementById('user-files').style.display = 'block';
  document.getElementById('user-submit').style.display = 'block';
  getStatus();
  var periodicStatus = setInterval(getStatus, 5000);
};



var getStatus = function() {
  console.log("getStatus");
  var fileList = []
  var configList = []
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     data = JSON.parse(this.responseText);
     for (var file_id in data) {
       if (!data.hasOwnProperty(file_id)) {
           //The current property is not a direct property of p
           continue;
       }
       //Do your logic with the property here
       configList = [];
       for (var Config in data[file_id]) {
         if (!data.hasOwnProperty(file_id)) {
             //The current property is not a direct property of p
             continue;
         }
         configList.push({"name": Config,
                          "camadas":data[file_id][Config]["Camadas"],
                          "duracao":data[file_id][Config]["Duracao"],
                          "filamento":data[file_id][Config]["Filamento"]});

       }
       if (configList.length > 0){
         var a= document.createElement('a');
         a.href= data[file_id]["High"]["url"];
         fileList.push({"file": file_id,
                        "configs": configList,
                        "url": data[file_id]["High"]["url"],
                        "filename":a.pathname.split('/').pop()})
       }

     }
     view_moustache = {"files": fileList};
     document.getElementById("user-files").innerHTML = Mustache.to_html(template_moustache,view_moustache);
   }
  };
  xhttp.open("GET", "https://fabproapi.tk/status/", true);
  xhttp.send();

}
/**
 * Displays the UI for a signed out user.
 */
var handleSignedOutUser = function() {
  document.getElementById('user-signed-in').style.display = 'none';
  document.getElementById('user-signed-out').style.display = 'block';
  ui.start('#firebaseui-container', uiConfig);
};

// Listen to change in auth state so it displays the correct UI for when
// the user is signed in or not.
firebase.auth().onAuthStateChanged(function(user) {
  // The observer is also triggered when the user's token has expired and is
  // automatically refreshed. In that case, the user hasn't changed so we should
  // not update the UI.
  if (user && user.uid == currentUid) {
    return;
  }
  document.getElementById('loading').style.display = 'none';
  document.getElementById('loaded').style.display = 'block';
  user ? handleSignedInUser(user) : handleSignedOutUser();
});


/**
 * Initializes the app.
 */
var initApp = function() {
  document.getElementById('sign-out').addEventListener('click', function() {
    firebase.auth().signOut();
  });
  document.getElementById('delete-account').addEventListener(
      'click', function() {
        firebase.auth().currentUser.delete();
      });
};


var Upload_File = function () {
  // File or Blob named mountains.jpg
var file = document.getElementById("arquivo").files[0];
var storageRef = firebase.storage().ref();

// Create the file metadata
var metadata = {
  contentType: 'application/sla'
};

// Upload file and metadata to the object 'images/mountains.jpg'
var uploadTask = storageRef.child('models/' + file.name).put(file, metadata);

// Listen for state changes, errors, and completion of the upload.
uploadTask.on(firebase.storage.TaskEvent.STATE_CHANGED, // or 'state_changed'
  function(snapshot) {
    // Get task progress, including the number of bytes uploaded and the total number of bytes to be uploaded
    var progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
    console.log('Upload is ' + progress + '% done');
    switch (snapshot.state) {
      case firebase.storage.TaskState.PAUSED: // or 'paused'
        console.log('Upload is paused');
        break;
      case firebase.storage.TaskState.RUNNING: // or 'running'
        console.log('Upload is running');
        break;
    }
  }, function(error) {
  switch (error.code) {
    case 'storage/unauthorized':
      // User doesn't have permission to access the object
      break;

    case 'storage/canceled':
      // User canceled the upload
      break;

    case 'storage/unknown':
      // Unknown error occurred, inspect error.serverResponse
      break;
  }
  }, function() {
    // Upload completed successfully, now we can get the download URL
    var downloadURL = uploadTask.snapshot.downloadURL;
    console.log(downloadURL);
    $.post( "https://fabproapi.tk/submit/", { 'URL': downloadURL} );
  });
}


window.addEventListener('load', initApp);
