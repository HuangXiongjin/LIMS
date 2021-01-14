<template>
    <el-row :gutter='20'>
       <el-col :span='24'>
            <div class="np" :style="conheight">没有访问的权限</div>
       </el-col>
    </el-row>
</template>
<script>
var moment=require('moment')
export default {
    data(){
        return {
            conheight:{
                height:''
            }
        }
    },
    created(){
      this.getHeight()
    },
    methods: {
       getHeight(){
          this.conheight.height=(window.innerHeight-220)+'px'
       },
    },
}
</script>
<style scoped>
    .np{
        padding-top: 80px;
        font-size: 36px;
        color:#666;
        text-align: center;
        background: #2D2D2D url('../assets/image/404np.jpg') no-repeat  center;

    }
</style>