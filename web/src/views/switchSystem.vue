<template>
  <el-row :gutter="20">
    <el-col :span="24">
      <el-col :span="6" v-for="(item,index) in systemOptions" :key="index">
        <div class="platformContainer cursor-pointer" style="text-align: center;" v-bind:class="{'color-lightgreen':index===systemActive}" @click="selectSystem(index,item.label)" @dblclick="dblclickSystem(index,item.label)">
          <p class="marginBottom text-size-48"><i :class="item.icon"></i></p>
          <p class="text-size-16">{{ item.label }}</p>
        </div>
      </el-col>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "switchSystem",
    props:["systemActive","systemOptions","defaultActiveUrl"],
    data(){
      return{

      }
    },
    mounted() {

    },
    methods:{
      selectSystem(index,label){
        this.systemOptions.forEach((item,i) =>{
          if(index === i){
            this.$emit("mainMenu",item.mainMenu)
            this.$emit("systemActive",index)
          }
        })
      },
      dblclickSystem(index,label){
        this.systemOptions.forEach((item,i) =>{
          if(index === i){
            if(item.mainMenu[0].children){
              this.$router.push(item.mainMenu[0].children[0].url)
            }else{
              this.$router.push(item.mainMenu[0].url)
            }
          }
        })
      }
    }
  }
</script>

<style scoped>

</style>
