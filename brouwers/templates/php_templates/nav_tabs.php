<?php foreach($nav as $k => $tab) { ?>
    <li id="tab-<?php echo $k; ?>" class="tab">
        <a href="<?php echo $tab['url']; ?>" title="<?php echo $tab['title']; ?>"
        	class="<?php echo $tab['classes']; ?>"><?php echo $tab['label'];?></a>
    </li>
<?php } ?>
<!--<li>
    <img src="{{ STATIC_URL }}images/nav/modelbouw_wiki.png" alt="Modelbouw Wiki"/>
</li>-->
<a href="<?php echo $settings['HONEYPOT_URL']; ?>" style="display: none;">ozone-inevitable</a>
