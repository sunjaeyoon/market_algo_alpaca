const nodemailer = require('nodemailer');
require('dotenv').config();

//process.env.USER_ID

var transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL_ADDRESS,
    pass: process.env.EMAIL_PASSWORD
  }
});

var mailOptions = {
  from: process.env.EMAIL_ADDRESS,
  to: process.env.EMAIL_DESTINATION,
  subject: 'Sending Email using Node.js',
  text: 'That was easy!'
};

transporter.sendMail(mailOptions, function(error, info){
  if (error) {
    console.log(error);
  } else {
    console.log('Email sent: ' + info.response);
  }
});