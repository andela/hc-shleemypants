$(function () {

    var MINUTE = {name: "minute", nsecs: 60};
    var HOUR = {name: "hour", nsecs: MINUTE.nsecs * 60};
    var DAY = {name: "day", nsecs: HOUR.nsecs * 24};
    var WEEK = {name: "week", nsecs: DAY.nsecs * 7};
    var UNITS = [WEEK, DAY, HOUR, MINUTE];

    var select = document.getElementById('input-select');
    var priorities = {}
    priorities[-2] = "Lowest";
    priorities[-1] =  "Low";
    priorities[0]  = "Normal";
    priorities[1]  = "High";
    priorities[2]  = "Emergency";

    for ([k,v] of Object.entries(priorities)) {
        var option   = document.createElement("option");
        option.text  = v;
        option.value = k;

        select.appendChild(option);
    }

    var secsToText = function(total) {
        var remainingSeconds = Math.floor(total);
        var result = "";
        for (var i=0, unit; unit=UNITS[i]; i++) {
            if (unit === WEEK && remainingSeconds % unit.nsecs != 0) {
                // Say "8 days" instead of "1 week 1 day"
                continue
            }

            var count = Math.floor(remainingSeconds / unit.nsecs);
            remainingSeconds = remainingSeconds % unit.nsecs;

            if (count == 1) {
                result += "1 " + unit.name + " ";
            }

            if (count > 1) {
                result += count + " " + unit.name + "s ";
            }
        }

        return result;
    }

    var periodSlider = document.getElementById("period-slider");
    noUiSlider.create(periodSlider, {
        start: [20],
        connect: "lower",
        range: {
            'min': [60, 60],
            '33%': [3600, 3600],
            '66%': [86400, 86400],
            '83%': [604800, 604800],
            'max': 2592000,
        },
        pips: {
            mode: 'values',
            values: [60, 1800, 3600, 43200, 86400, 604800, 2592000],
            density: 4,
            format: {
                to: secsToText,
                from: function() {}
            }
        }
    });

    periodSlider.noUiSlider.on("update", function(a, b, value) {
        var rounded = Math.round(value);
        $("#period-slider-value").text(secsToText(rounded));
        $("#update-timeout-timeout").val(rounded);
    });


    var graceSlider = document.getElementById("grace-slider");
    noUiSlider.create(graceSlider, {
        start: [20],
        connect: "lower",
        range: {
            'min': [60, 60],
            '33%': [3600, 3600],
            '66%': [86400, 86400],
            '83%': [604800, 604800],
            'max': 2592000,
        },
        pips: {
            mode: 'values',
            values: [60, 1800, 3600, 43200, 86400, 604800, 2592000],
            density: 4,
            format: {
                to: secsToText,
                from: function() {}
            }
        }
    });

    graceSlider.noUiSlider.on("update", function(a, b, value) {
        var rounded = Math.round(value);
        $("#grace-slider-value").text(secsToText(rounded));
        $("#update-timeout-grace").val(rounded);
    });

    var nagSlider = document.getElementById("nag-slider");
    noUiSlider.create(nagSlider, {
        start: [20],
        connect: "lower",
        range: {
            'min': [60, 60],
            '33%': [3600, 3600],
            '66%': [86400, 86400],
            '83%': [604800, 604800],
            'max': 2592000,
        },
        pips: {
            mode: 'values',
            values: [60, 1800, 3600, 43200, 86400, 604800, 2592000],
            density: 4,
            format: {
                to: secsToText,
                from: function() {}
            }
        }
    });

    nagSlider.noUiSlider.on("update", function(a, b, value) {
        var rounded = Math.round(value);
        $("#nag-slider-value").text(secsToText(rounded));
        $("#update-timeout-nag").val(rounded);
    });


    $('[data-toggle="tooltip"]').tooltip();

    $(".my-checks-name").click(function() {
        var $this = $(this);

        $("#update-name-form").attr("action", $this.data("url"));
        $("#update-name-input").val($this.data("name"));
        $("#update-tags-input").val($this.data("tags"));
        $("#update-departments-input").val($this.data("departments"));
        $('#update-name-modal').modal("show");
        $("#update-name-input").focus();

        return false;
    });

    $(".timeout-grace").click(function() {
        var $this = $(this);

        $("#update-timeout-form").attr("action", $this.data("url"));
        periodSlider.noUiSlider.set($this.data("timeout"))
        graceSlider.noUiSlider.set($this.data("grace"))
        nagSlider.noUiSlider.set($this.data("nag"))   
        $('#update-timeout-modal').modal({"show":true, "backdrop":"static"});

        return false;
    });

    $(".check-menu-remove").click(function() {
        var $this = $(this);

        $("#remove-check-form").attr("action", $this.data("url"));
        $(".remove-check-name").text($this.data("name"));
        $('#remove-check-modal').modal("show");

        return false;
    });


    $("#my-checks-tags button").click(function() {
        // .active has not been updated yet by bootstrap code,
        // so cannot use it
        $(this).toggleClass('checked');

        // Make a list of currently checked tags:
        var checked = [];
        $("#my-checks-tags button.checked").each(function(index, el) {
            checked.push(el.textContent);
        });

        // No checked tags: show all
        if (checked.length == 0) {
            $("#checks-table tr.checks-row").show();
            $("#checks-list > li").show();
            return;
        }

        function applyFilters(index, element) {
            var tags = $(".my-checks-name", element).data("tags").split(" ");
            for (var i=0, tag; tag=checked[i]; i++) {
                if (tags.indexOf(tag) == -1) {
                    $(element).hide();
                    return;
                }
            }

            $(element).show();
        }

        // Desktop: for each row, see if it needs to be shown or hidden
        $("#checks-table tr.checks-row").each(applyFilters);
        // Mobile: for each list item, see if it needs to be shown or hidden
        $("#checks-list > li").each(applyFilters);

    });

    $("#my-checks-departments button").click(function() {


        console.log("This is the awesome department i was talkkn about")
        // .active has not been updated yet by bootstrap code,
        // so cannot use it
        $(this).toggleClass('checked');

        // Make a list of currently checked departments:
        var checked = [];
        $("#my-checks-departments button.checked").each(function(index, el) {
            checked.push(el.textContent);
        });

        // No checked tags: show all
        if (checked.length == 0) {
            $("#checks-table tr.checks-row").show();
            $("#checks-list > li").show();
            return;
        }

        function applyFilters(index, element) {
            var departments = $(".my-checks-name", element).data("departments").split(" ");
            for (var i=0, department; department=checked[i]; i++) {
                if (departments.indexOf(department) == -1) {
                    $(element).hide();
                    return;
                }
            }

            $(element).show();
        }

        // Desktop: for each row, see if it needs to be shown or hidden
        $("#checks-table tr.checks-row").each(applyFilters);
        // Mobile: for each list item, see if it needs to be shown or hidden
        $("#checks-list > li").each(applyFilters);

    });

    $(".pause-check").click(function(e) {
        var url = e.target.getAttribute("data-url");
        $("#pause-form").attr("action", url).submit();
        return false;
    });


    $(".usage-examples").click(function(e) {
        var a = e.target;
        var url = a.getAttribute("data-url");
        var email = a.getAttribute("data-email");

        $(".ex", "#show-usage-modal").text(url);
        $(".em", "#show-usage-modal").text(email);

        $("#show-usage-modal").modal("show");
        return false;
    });


    var clipboard = new Clipboard('button.copy-link');
    $("button.copy-link").mouseout(function(e) {
        setTimeout(function() {
            e.target.textContent = "copy";
        }, 300);
    })

    clipboard.on('success', function(e) {
        e.trigger.textContent = "copied!";
        e.clearSelection();
    });

    clipboard.on('error', function(e) {
        var text = e.trigger.getAttribute("data-clipboard-text");
        prompt("Press Ctrl+C to select:", text)
    });

    $(".priority-cell").click(function() {
        var $this = $(this);
        var buttonPriority = $this.find("button").data("url")
        $("#update-priority-form").attr("action", buttonPriority)
        var priorityNbr = $this.find("button").data("priority")
        $("#priority-slider").attr("data-sliderstart", priorityNbr)
        $("#input-select").val(priorityNbr)
        // Slider
        //Creating a Slider to  display the different priorities
    var priorityslider = document.getElementById('priority-slider');
    var startSlider = $("#priority-slider");

    noUiSlider.create(priorityslider, {
        start: [startSlider.attr("data-sliderstart")],
        connect: "lower",
        range: {
            min: -2,
            max: 2
        },
        pips:{
            mode: "values",
            values: [-2,-1,0,1,2],
            density: 100

        }
    }, true);

    priorityslider.noUiSlider.on('update', function( values, handle ) {
        var value = values[handle];

        if ( handle ) {
            inputPriority.value = value;
        } else {
            select.value = Math.round(value);
        }
    });

    select.addEventListener('change', function(){
        priorityslider.noUiSlider.set([this.value, null]);
    });
        // Slider
        $("#priority-modal").modal({ show: true, backdrop: "static" });
        $("#show-advanced-time").modal("hide");

        return false;
    });

    $(".destroySlider").click(function(){
        var priorityslider = document.getElementById('priority-slider');
        priorityslider.noUiSlider.destroy()
    });


});
