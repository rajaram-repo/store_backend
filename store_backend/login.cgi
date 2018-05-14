use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use Crypt::Password;

##---------------------------- MAIN ---------------------------------------

my $q;
if(authenticate_user()) {
    send_to_main();   
    }
else {
    send_to_login_error();
    }    
###########################################################################

###########################################################################
sub authenticate_user {
    $q = new CGI;
    my $user = $q->param("user");
    my $password = $q->param("password");    
    open DATA, "</srv/www/cgi-bin/jadrn047/proj1/passwords.dat" 
        or die "Cannot open file.";
    @file_lines = <DATA>;
    close DATA;

    $OK = 0; #not authorized

    foreach $line (@file_lines) {
        chomp $line;
        ($stored_user, $stored_pass) = split /=/, $line;    
    if($stored_user eq $user && check_password($stored_pass, $password)) {
        $OK = 1;
        last;
        }
    }
          
    return $OK;
    }
###########################################################################

###########################################################################
sub send_to_login_error {
    print <<END;
Content-type:  text/html

<html>
<head>
    <meta http-equiv="refresh" 
        content="0; url=http://jadran.sdsu.edu/~jadrn047/proj1/error.html" />
</head><body></body>
</html>

END
    }  
    
###########################################################################
      
###########################################################################
sub send_to_main {
# args are DRIVER, CGI OBJECT, SESSION LOCATION
# default for undef is FILE, NEW SESSION, /TMP 
# for login.html, don't look for any existing session.
# Always start a new one.  Send a cookie to the browser.
# Default expiration is when the browser is closed.
# WATCH YOUR COOKIE NAMES! USE JADRNXXX_SID  
    my $session = new CGI::Session(undef, undef, {Directory=>'/tmp'});
    $session->expires('+1d');
    my $cookie = $q->cookie(jadrn047SID => $session->id);
    print $q->header( -cookie=>$cookie ); #send cookie with session ID to browser    
    my $sid = $session->id;
    print <<END;
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Bootstrap Example</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <link rel="stylesheet" href="/~jadrn047/proj1/mycss.css">
  <script src="/jquery/jquery.js"></script>
  <script src="/jquery/jQueryUI.js"></script>    
  <script src="/~jadrn047/proj1/myjs.js"></script>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>

<!-- <div class="container">
  <h3>Vertical Pills</h3>
  <div class="row">
    <div class="col-md-3">
      <ul class="nav nav-pills nav-stacked">
        <li class="active"><a href="#">Home</a></li>
        <li><a href="#">Menu 1</a></li>
        <li><a href="#">Menu 2</a></li>
        <li><a href="#">Menu 3</a></li>
      </ul>
    </div>
    <div class="col-md-3">
      <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
    </div>
    <div class="col-md-3"> 
      <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
    </div>
    <div class="col-md-3"> 
      <p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam.</p>
    </div>
    <div class="clearfix visible-lg"></div>
  </div>
</div> -->
<h1>Data Management Tool</h1>

<ul class="nav nav-pills nav-stacked col-md-2" id="myTab" role="tablist">
  <li class="nav-item">
    <a class="nav-link active text-center" id="add-tab" data-toggle="tab" href="#add" role="tab" aria-controls="add" aria-selected="true">Add</a>
  </li>
  <li class="nav-item">
    <a class="nav-link text-center" id="profile-tab" data-toggle="tab" href="#profile" role="tab" aria-controls="profile" aria-selected="false">Edit</a>
  </li>
  <li class="nav-item">
    <a class="nav-link text-center" id="messages-tab" data-toggle="tab" href="#messages" role="tab" aria-controls="messages" aria-selected="false">Delete</a>
  </li>
</ul>

<!-- Tab panes -->
<div class="tab-content col-md-10">
  <div class="tab-pane active" id="add" role="tabpanel" aria-labelledby="add-tab">
    <h3>ADD NEW RECORD</h3>
    <form method="post" 
      enctype="multipart/form-data" 
      name="myform"
      action="">
      <div class = "col-md-8" >
        <p>
            <div class="form-group">
              <label class="col-sm-2 col-form-label" for="sku">SKU:</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" name="sku" id="sku" size="7" placeholder="Enter sku">
              </div>
            </div>
            <div class="form-group">
              <label class="col-sm-2 col-form-label" for="cat">CatID:</label>
              <div class="col-sm-10">
                <select class="form-control" name="cat" id="cat">
                  <option value="1">DSLR</option>
                  <option value="2">Point and Shoot</option>
                  <option value="3">Advanced Amateur</option>
                  <option value="4">Underwater</option>
                  <option value="5">Film</option>
                  <option value="6">mirrorless</option>
                  <option value="7">superzoom</option>
                </select>
              </div>
            </div>
            <!-- <h3 id="status"></h3> -->

           <div class="form-group">
              <label class="col-sm-2 col-form-label" for="ven">VendorID:</label>
              <div class="col-sm-10">
                <select class="form-control" name="ven" id="ven">
                  <option value="1">Nikon</option>
                  <option value="2">Canon</option>
                  <option value="3">Olympus</option>
                  <option value="4">Lumix</option>
                  <option value="5">Pentax</option>
                  <option value="6">Leica</option>
                  <option value="7">Sony</option>
                  <option value="8">Fuji</option>
                </select>
              </div>
            </div>


           <div class="form-group">
            <label class="col-sm-2 col-form-label" for="ven_model">VendorModel:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" name="ven_model" id="ven_model" size="20" placeholder="Enter Vendor Model">
            </div>
          </div>

          <div class="form-group">
            <label class="col-sm-2 col-form-label" for="desc">Description:</label>
            <div class="col-sm-10">
              <textarea type="text" class="form-control" name="desc" id="desc" size="50" placeholder="Enter Description"></textarea>
            </div>
          </div>

          <div class="form-group">
            <label class="col-sm-2 col-form-label" for="feature">Feature:</label>
            <div class="col-sm-10">
              <textarea type="text" class="form-control" name="feature" id="feature" size="50" placeholder="Enter Features"></textarea>
            </div>
          </div>

          <div class="form-group">
            <label class="col-sm-2 col-form-label" for="cost">Cost:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" name="cost" id="cost" size="10" placeholder="Enter Cost">
            </div>
          </div>

          <div class="form-group">
            <label class="col-sm-2 col-form-label" for="retail">Retail:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" name="retail" id="retail" size="10" placeholder="Enter Retail">
            </div>
          </div>

          <div class="form-group">
            <label class="col-sm-2 col-form-label" for="quant">Quantity:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" name="quant" id="quant" size="10" placeholder="Enter Retail">
            </div>
          </div>       

            <h3 id="status_1"></h3>
            <h3 id="error"></h3>
            <input class="btn btn-success" type="button" value="Upload Data" id="submit_button" />
        </p>
        </div>
        <div class="col-md-4">
          <label class="col-form-label" for="product_image">Image to upload:</label>
          <div>
            <input type="file" name="product_image" id="product_image" />
          </div>
          <img id="blah" src="#" alt="your image appears here"/> 
        </div>  
    </form>
    <br>
    <br>
  </div>

  <div class="tab-pane" id="profile" role="tabpanel" aria-labelledby="profile-tab">
    <p>
      <h3>EDIT RECORD</h3>
      <label class="col-sm-1 col-form-label" for="sku_edit">SKU:</label>
      <div class="col-sm-5">
        <input type="text" class="form-control" name="sku_edit" id="sku_edit" size="10" placeholder="Enter SKU to search">
      </div>
      <input class="btn btn-primary col-sm-2" type="button" value="Fetch" id="fetch_button" />
      <span class="col-sm-offset-4"></span>

      <form method="post" 
            enctype="multipart/form-data" 
            name="myform_e"
            action="">
        <div class = "col-md-8" >
          <p>
            <div class="form-group">
              <label class="col-sm-2 col-form-label" for="sku_e">SKU:</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" name="sku_e" id="sku_e" size="7" placeholder="Enter sku" disabled>
              </div>
            </div>
            <div class="form-group">
              <label class="col-sm-2 col-form-label" for="cat_e">CatID:</label>
              <div class="col-sm-10">
                <select class="form-control" name="cat_e" id="cat_e">
                  <option value="1">DSLR</option>
                  <option value="2">Point and Shoot</option>
                  <option value="3">Advanced Amateur</option>
                  <option value="4">Underwater</option>
                  <option value="5">Film</option>
                  <option value="6">mirrorless</option>
                  <option value="7">superzoom</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label class="col-sm-2 col-form-label" for="ven_e">VendorID:</label>
              <div class="col-sm-10">
                <select class="form-control" name="ven_e" id="ven_e">
                  <option value="1">Nikon</option>
                  <option value="2">Canon</option>
                  <option value="3">Olympus</option>
                  <option value="4">Lumix</option>
                  <option value="5">Pentax</option>
                  <option value="6">Leica</option>
                  <option value="7">Sony</option>
                  <option value="8">Fuji</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label class="col-sm-2 col-form-label" for="ven_model_e">VendorModel:</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" name="ven_model_e" id="ven_model_e" size="20" placeholder="Enter Vendor Model">
              </div>
            </div>
            <div class="form-group">
              <label class="col-sm-2 col-form-label" for="desc_e">Description:</label>
              <div class="col-sm-10">
                <textarea type="text" class="form-control" name="desc_e" id="desc_e" size="50" placeholder="Enter Description"></textarea>
              </div>
            </div>
            <div class="form-group">
              <label class="col-sm-2 col-form-label" for="feature_e">Feature:</label>
              <div class="col-sm-10">
                <textarea type="text" class="form-control" name="feature_e" id="feature_e" size="50" placeholder="Enter Features"></textarea>
              </div>
            </div>
            <div class="form-group">
              <label class="col-sm-2 col-form-label" for="cost_e">Cost:</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" name="cost_e" id="cost_e" size="10" placeholder="Enter Cost">
              </div>
            </div>
            <div class="form-group">
              <label class="col-sm-2 col-form-label" for="retail_e">Retail:</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" name="retail_e" id="retail_e" size="10" placeholder="Enter Retail">
              </div>
            </div>
            <div class="form-group">
              <label class="col-sm-2 col-form-label" for="quant_e">Quantity:</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" name="quant_e" id="quant_e" size="10" placeholder="Enter Retail">
              </div>
            </div>
            <input class="btn btn-warning" type="button" value="Update Record" id="submit_button_e" />
            <h3 id="status_1_e"></h3>
            <h3 id="error_e"></h3>
          </p>
        </div>
        <div class="col-md-4">
          <h3 id="pic_e"></h3>
          <label class="col-form-label" for="quant">Update image:</label>
          <div>
            <input type="file" name="product_image_e" id="product_image_e" />
          </div>
          <!-- <img id="blah" src="#" alt="your image appears here" />  -->
        </div>  
      </form>
      
      <p id="raw"></p>
      <p id="data"></p>
    </p>
  </div>
  <div class="tab-pane" id="messages" role="tabpanel" aria-labelledby="messages-tab">
    <p>
      <label class="col-sm-1 col-form-label" for="sku_d">SKU:</label>
      <div class="col-sm-5">
        <input type="text" class="form-control" name="sku_d" id="sku_d" size="10" placeholder="Enter SKU to delete">
      </div>
      <input class="btn btn-danger col-sm-2" type="button" value="Delete Record" id="delete_button" />
      <h3 id="status_d"></h3>
    </p>
  </div>
</div>

</body>
</html>

END
}
###########################################################################    