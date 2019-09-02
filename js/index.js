// var
var course_dict,
    college_dict,
    college_data;

// main
$.ajaxSettings.async = false;
$.getJSON("https://raw.githubusercontent.com/DieYiSu/CCU_Course_query/master/source/all_course_dict.json", data => course_dict = data);
$.getJSON("https://raw.githubusercontent.com/DieYiSu/CCU_Course_query/master/source/college_dict.json", data => college_dict = data);
$.getJSON("https://raw.githubusercontent.com/DieYiSu/CCU_Course_query/master/source/data.json", data => college_data = data);

let app = new Vue({
    el: '#vue_app',
    data: {
        course_dict: course_dict,
        new_course_dict: course_dict,
        college_dict: college_dict,
        college_data: college_data,
        search: ""
    },
    methods : {
        search_result: function(){
            this.new_course_dict =  this.course_dict.filter(course => {
                return Object.values(course).includes(this.search)
            })
        }
    },
    computed: {
    }, 
    watch : {
    }
});
