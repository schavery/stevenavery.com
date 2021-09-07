<?php

/*
Handle SMS forwarding from Twilio
*/

header('Content-Type: text/html');
$count = $_REQUEST['NumMedia'] || 0;
?>
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message to="7075361863">
<?php echo $_REQUEST['From'] . ': ' . $_REQUEST['Body']; ?>
<?php for($i = 0; $i < $count; $i++) { ?>
    <Media><?php echo $_REQUEST['MediaUrl' . $i]; ?></Media>
<?php } ?>
  </Message>
</Response>

<?php
// mail('schavery@gmail.com', 'SMS from ' . $_REQUEST['From'], print_r($_REQUEST, true), 'From: captain@stevenavery.com'); ?>

