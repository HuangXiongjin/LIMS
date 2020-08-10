<template>
  <el-row :gutter="15">
    <el-col :span="24" v-if="!showDragBoard">
      <el-form :inline="true">
        <el-form-item>
          <el-button @click="showDragBoard = true">调整看板</el-button>
        </el-form-item>
      </el-form>
    </el-col>
    <el-col :span="24" v-if="showDragBoard">
      <el-form :inline="true">
        <el-form-item>
          <el-button @click="showDragBoard = false">调整完成</el-button>
        </el-form-item>
      </el-form>
      <el-row :gutter="15">
        <el-col :span="18" style="min-height: 400px">
          <draggable :list="list1" :options="{group:'article', disabled: disabled,sort: true}"
             @start="start22"
             @end="end22" class="dragArea11" style="height: 400px;">
            <el-col :span="item.col" v-for="(item, index) in list1" :key="index">
              <div class="container-col">
                <p>{{item.name}}</p>
                <i class="el-icon-delete" @click="handleDel(index, item.id)"></i>
              </div>
            </el-col>
          </draggable>
        </el-col>
        <el-col :span="6">
          <draggable :list="list2" :options="{group:{name: falgs,pull:'clone'},filter:'.undraggable', sort: true}"
             @end="end" class="dragArea">
            <el-col :span="item.col" v-for="item in list2" :key="item.id" :class="{undraggable : item.flag}" class="list-complete-item">
              <div class="container-col">
                <p>{{item.name}}</p>
              </div>
            </el-col>
          </draggable>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>
<script>
  import draggable from 'vuedraggable'
  var moment = require('moment');
  export default {
    name: "index",
    components:{draggable},
    data(){
      return {
        showDragBoard:false,
        falgs: 'article',
        disabled: false,
        list1: [],
        list2: [
          {id: 1, name:"预览",col:6},
          {id: 2, name:"预警",col:6},
          {id: 3, name:"排名",col:18},
          {id: 4, name:"生产",col:12},
          {id: 5, name:"设备",col:12},
          {id: 6, name:"排产",col:12},
　　　　　]
      }
    },
    created(){

    },
    watch:{

    },
    computed:{ //计算属性

    },
    methods: {
      end (ev) {
        if (ev.to.className === 'dragArea11') {
          this.$set(this.list2[ev.oldIndex], 'flag', true)
        }
      },
      start22 (event) {
        this.falgs = '222222'
      },
      end22 (ev) {
        this.falgs = 'article'
      },
      handleDel (index, id) {
        this.list1.splice(index, 1)
        let q = this.list2.find((value, index, arr) => {
          return value.id === id
        })
        this.$set(q, 'flag', false)
      }
    }
  }
</script>
<style scoped>
  .container-col{
    clear: both;
    overflow: hidden;
    border: 1px solid #a1a1a1;
    border-radius: 4px;
    padding: 15px;
    margin-bottom: 15px;
    height: 50px;
  }
  .list-complete-item {
    cursor: pointer;
    position: relative;
  }
  .list-complete-item.sortable-chosen {
    color: #4AB7BD;
  }
  .list-complete-item.sortable-ghost {
    color: #30B08F;
  }
  .undraggable {
    color: red;
  }
  .list-complete-enter,.list-complete-leave-active {
    opacity: 0;
  }
</style>
