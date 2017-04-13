$(document).ready(function(){
    $(".datepicker").datepicker({
        dateFormat:'yy-mm-dd',
        changeMonth: true,
        changeYear: true,
        minDate: new Date(1900,00,01),
        maxDate: +0,
        yearRange:'1900:'
    });
  });