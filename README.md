# zandro_rcon
Zandronum RCon console made with python (3.8)

<h1>How to use</h1>
<ol>
<li>Import into your python file</li>
<li>Instance the 'Zandronum' class with ip (str), port (int) and rcon password (str) as the parameters</li>
<li>If you successfully connect the 'state' variable will be changed to 'Connected'</li>
<li>If the password is invalid its state will change to 'Invalid'</li>
</ol>
<br>
<ul>
<li>If you want to send a command call 'send_command' with a string argument as the command</li>
<li>If you need to disconnect from the server, call 'disconnect'</li>
</ul>
<br>
<h5>The latest lines of the log are saved in 'currentLog'</h5>
<h6>Any doubts, yell at Bull Gator#2394</h6>
