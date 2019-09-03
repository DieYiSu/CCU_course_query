// var
var course_dict,
    college_dict,
    college_data;

// main
$.ajaxSettings.async = false;
// $.getJSON("https://raw.githubusercontent.com/DieYiSu/CCU_Course_query/master/source/all_course_dict.json", data => course_dict = data);
$.getJSON("source/all_course_dict.json", data => course_dict = data);
$.getJSON("source/college_dict.json", data => college_dict = data);
$.getJSON("source/data.json", data => college_data = data);

Vue.component('course-card', {
    props: ['card_info'],
    template : `#courseCardTemplate`, 
    data : () => {
        return {
            grade_color : ['bg-primary text-white', 'bg-info text-white', 'bg-warning text-white', 'bg-danger text-white'], 
            bg_color : '', 
            course_detail : null
        }
    }, 
    methods : {
        detail : function(){
            this.$emit('emit_detail', this.card_info)
        }
    },
    computed : {
        color : function(){
            if(typeof this.card_info.年級 === "undefined"){
                return `bg-dark text-white`
            }else {
                return this.grade_color[this.card_info.年級-1]
            }
        }
    }
})

let app = new Vue({
    el: '#vue_app',
    data: {
        course_dict: course_dict,
        new_course_dict: course_dict,
        college_dict: college_dict,
        college_data: college_data,
        search: "", 
        main_course_detail : ''

    },
    methods : {
        search_result: function(){
            if(this.search != ""){
                this.new_course_dict =  this.course_dict.filter(course => {
                    return Object.values(course).includes(this.search) 
                })
            }else {
                this.new_course_dict = this.course_dict
            }
        }, 
        reveice_course_detail : function(card_info){
            this.main_course_detail = card_info;
        }
    },
    computed : {
    }
});
