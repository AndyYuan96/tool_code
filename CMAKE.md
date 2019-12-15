# CMAKE

作用：

​	主要区分cmake,make,gcc,g++,GCC.

​	GCC: Gun Compiler Collection,它可以编译多种语言，C++，C等等。

​	gcc是GCC中的GUN C Compiler(c语言编译器)

​	g++是GCC中的GUN C++ Compiler(C++编译器)

​	如果只有一两个文件，直接使用gcc main.cpp -o out 即可，如果有多个文件，并且相互依赖，如果还想用g++/gcc编译的话，可以使用Makefile和make, make是GCC提供的编译工具，它根据Makefile来处理各种依赖关系，本来这个Makefile需要人来自己写，但是太麻烦，就出现了CMake,CMake根据CMakeList.txt生成Makefile文件，人只需要写CMakeList.txt中的高级语言即可。



​	

```
cmake_minimum_required(VERSION 2.8)
project(foo)
add_executable(foo foo.cpp) #根据平台不同生成.exe后缀，linux没后缀。
```

```
#_builds是生成的文件夹的名字，改了CMakeLists.txt之后不用在一个cmake ..了，直接编译就行：cmake --build _builds
cmake -H. -B_builds
```



### CMake policies

```
当更新cmake版本之后，想用原来的特性： cmake_policy(SET CMP0038 OLD)
```



### CMake project

```
project(foo)会把默认语言设置成C和C++,并声明一些变量foo_*，并执行一些基础的编译工具检查。

执行完后会设置：
${CMAKE_C_COMPILER}
${CMAKE_CXX_COMPILER}

要把自己的检查放在project()之后

如果只想支持C project(foo C), 这样就不会设置${CMAKE_CXX_COMPILER}，这样就不能在编译cpp文件
project(foo NONE) 不支持任何语言
project(foo LANGUAGES C)
project(foo LANGUAGES NONE)


project()会声明*_{SOURCE,BINARY}_DIR变量
project(foo VERSION 1.2.7) 可以指定版本 ${PROJECT_VERSION}
可以不使用PROJECT_*,直接使用名字foo_{SOURCE,BINARY}_DIR

下层的CMakeList.txt可以访问上层的CMakeList.txt中的变量：
上层：
cmake_minimum_required(VERSION 2.8)
project(foo)
message("From top level:")
message(" Source (general): ${PROJECT_SOURCE_DIR}")
message(" Source (foo): ${foo_SOURCE_DIR}")
add_subdirectory(boo)

下层：
cmake_minimum_required(VERSION 2.8)
project(boo)
message("From subdirectory 'boo':")
message(" Source (general): ${PROJECT_SOURCE_DIR}")
message(" Source (foo): ${foo_SOURCE_DIR}")
message(" Source (boo): ${boo_SOURCE_DIR}")

如果在顶层没有写project() 那么CMake会在cmake_minimum_required之前调用project()进行一系列声明
```



### Variable

```
cache variable 和 regular(normal) variable的区别： regular的有scope,并且在每次运行cmake时都会重新生成，cache只在第一次运行的时候生成，第二次使用第一次的值。
cmake_minimum_required(VERSION 2.8)
project(foo NONE)
message("Regular variable (before): ${abc}")
message("Cache variable (before): ${xyz}")
set(abc "123")
set(xyz "321" CACHE STRING "")
message("Regular variable (after): ${abc}")
message("Cache variable (after): ${xyz}")

每个regular variable都会被链接到它定义时的scope.
add_subdirectory 和 function 会引入他们自己的scope
就是你在add_subdirectory()的CmakeLists.txt 新定义了一个变量，与上层的一个变量重名，就会覆盖上层变量的值。
当一个新的scope被创建的时候，会继承父group的变量。

比如你加了两个add_subdirectory(), 那么这两个sub都会继承foo的变量abc,并初始化它为foo中abc的值。

unset()可以将variable从当前scope中移除，${}这个变量会返回空string.

include()和macro不会引入新的scope
include("modify_xyz.cmake") 在modify_xyz.cmake中改变了xyz,在当前scope中xyz也会改变。

子group可以给父group中的变量赋值 ： set(abc "666" PARENT_SCOPE)
但该值在当前子group中的值不受影响。

如果当前scope中没有这个变量，cmake会从cache中寻找。
要注意两者的顺序：
set(a "789" CACHE STRING "")
set(a "123")
这样unset()之后会从cache中寻找

set(a "123")
set(a "789" CACHE STRING "")
这样当调用set(  CACHE)的时候就已经unset(a)了
# set(a "789" CACHE STRING "") 只会影响当前scope，不会影响父scope中a的值。

变量的名字区分大小写，并且支持任何字符。

当创建新变量的时候可以使用${}已存在的变量

${}可以嵌套使用 ： ${CMAKE_${lang}_COMPILER}

变量的类型只有字符串，但是不同的命令可以不同的解释它们。比如说if可以把字符串当作布尔，路径，target name等等。

cmake_minimum_required(VERSION 2.8)
project(foo)
set(condition_a "TRUE")
set(condition_b "NO")
set(path_to_this "${CMAKE_CURRENT_SOURCE_DIR}/CMakeLists.txt")
set(target_name foo)
add_library("${target_name}" foo.cpp)
if(condition_a)
message("condition_a")
else()
message("NOT condition_a")
endif()
if(condition_b)
message("condition_b")
else()
message("NOT condition_b")
endif()
if(EXISTS "${path_to_this}")
message("File exists: ${path_to_this}")
else()
message("File not exist: ${path_to_this}")
endif()
if(TARGET "${target_name}")  exe 或 library都是TARGET
message("Target exists: ${target_name}")
else()
message("Target not exist: ${target_name}")
endif()

set可以创建一个list
set(10 a b c) -> a;b;c
set(11 a;b;c) -> a;b;c
set(14 a "b;c") -> a;b;c

访问list元素与获得长度
list(LENGTH 10 10_len)
list(GET 10 2 10_2)
list(REMOVE_AT 10 0)
list(APPEND list_name element)

Cache变量是全局的，在子scope中设置的cache变量，父scope也可以看到。
两次设置Cache变量，只有第一次的有用.
set(abc "123" CACHE STRING "")
set(abc "456" CACHE STRING "") 没用
cmake -Dabc=4 会比CmakeLists.txt中的cache优先级高

强制第二次设置cache
set(abc "123" CACHE STRING "" FORCE) # 记住使用set CACH之后会unset同名变量，只当set CACHE起作用的时候。

Cache变量可以在gui中进行提示：
set(FOO_A "YES" CACHE BOOL "Variable A")
set(FOO_B "boo/info.txt" CACHE FILEPATH "Variable B")
set(FOO_C "boo/" CACHE PATH "Variable C")
set(FOO_D "abc" CACHE STRING "Variable D")
message("FOO_A (bool): ${FOO_A}")
message("FOO_B (file path): ${FOO_B}")
message("FOO_C (dir path): ${FOO_C}")
message("FOO_D (string): ${FOO_D}")

unset(x CACHE) 移除CACHE变量

CMakeLists.txt中可以读入环境变量： $ENV{}
$ENV{USERNAME}
set(ENV{USERNAME} "zilong") 设置环境变量
unset(ENV{USERNAME}) 取消环境变量
子scope会继承父scope设置的环境变量

set()的环境变量是在configure阶段生效的，但是当编译的时候，环境变量还是原来环境中的变量。
CMake不会追踪环境变量的改变，想要改变的环境变量在编译的时候生效 
想要环境变量改变时刻生效：
set(target_name "$ENV{ABC}-tgt")
add_executable("${target_name}" foo.cpp)
尽量不要依赖会改变的环境变量
```

### CMake listfiles

```
CMake代码可以存在哪里：
1.CMakeLists.txt以及add_subdirectory()目录中的CMakeLists.txt
2.*.cmake文件，可以复用一些代码

顶端的CMakeLists.txt是树的根节点，add_subdirectory()是它的子节点。
${CMAKE_SOURCE_DIR} 在任何节点都是代表顶端CmakeLists.txt的根目录。
${CMAKE_CURRENT_SOURCE_DIR} 代表当前节点的跟目录
同理SOURCE 可以换成 BINARY

CMake modules是一个复用代码非常方便的事情。
对CMAKE_MODULE_PATH更改加入自己的CMake modules
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/modules")
include(MyModule)

Common variable: 每个CmakeLists.txt都有这种变量。
CMAKE_CURRENT_LIST_DIR: 当前正在处理的文件所在的目录 
CMAKE_CURRENT_LIST_FILE： 当前正在处理的文件的绝对路径
CMAKE_SOURCE_DIR: 根节点的目录
CMAKE_BINARY_DIR:
PROJECT_SOURCE/BINARY_DIR : 当前CMakeLists.txt所属的project的路径
CMAKE_CURRENT_SOURCE/BINARY_DIR : 子节点的目录
```

### CMake 结构

```
set(C "OFF")
set(D "ON")

if(C)
  message("Condition 5")
elseif(D)
  message("Condition 6")
else()
  message("Condition 7")
endif()

for循环：
set(mylist "foo" "boo" "bar")
foreach(x ${mylist})
  message(" ${x}")
endforeach()

set(combined_list "${mylist}" "x;y;z")
foreach(x ${combined_list})
   message(" ${x}")
endforeach()

message("Simple range:")
foreach(x RANGE 10)
	message(" ${x}")
endforeach()
	message("Range with limits:")
foreach(x RANGE 3 8)
	message(" ${x}")
endforeach()
message("Range with step:")
foreach(x RANGE 10 14 2)
message(" ${x}")
endforeach()

while:
while(CONDITION)

break()
continue()

函数：
没有参数：
function(foo)
message("Calling 'foo' function")
endfunction()
有参数：
function(boo x y z)
message("Calling function 'boo':")
message(" x = ${ARGV0}")
message(" y = ${ARGV1}")
message(" z = ${ARGV2}")
message(" total = ${ARGC}")
endfunction()

return()退出函数
CMAKE_CURRENT_LIST_DIR在函数中的值：
当一个文件调用一个函数时，要先include()这个函数
然后运行这个函数时，CMAKE_CURRENT_LIST_DIR的值是调用这个函数的文件的CMAKE_CURRENT_LIST_DIR,而不是这个函数定义的文件的CMAKE_CURRENT_LIST_DIR



```

### Cmake Executables

```
Targets是全局的， 不能声明两个名字一样的target,即使在两个CMakeLists.txt文件中。
add_executable(foo main.cpp)
```



### Cmake Tests

```
如果现在我们有多个可执行文件，想要一起测试他们而不是一个个的运行，可以使用CTest工具。
相关的命令为：
	ctest : 运行test
	add_test()： 在CmakeLists.txt中加入测试
	enable_testing()： 允许生成测试文件，只有使用这句ctest才能用。

cmake_minimum_required(VERSION 2.8)
project(foo)
add_executable(boo boo.cpp)
add_executable(bar bar.cpp)
enable_testing()
add_test(NAME boo COMMAND boo)
add_test(NAME bar COMMAND bar)
add_test(NAME bar-with-args COMMAND bar arg1 arg2 arg3)

默认ctest只会显示通过或失败，可以使用-V显示详细输出就像真的运行这个程序。
ctest -R name 只执行某个可执行文件的测试
```

### Cmake Libraries

```
static library:
	你使用了某个库的函数，那么这些函数代码二进制都拷贝到你的代码程序中，这样运行时可以直接找到这些函数，可以在没有这些库的机器上运行。
shared library:
	只是记住了库函数的地址，在运行的时候程序自己按地址加载函数代码。

#在生成库的时候不想生成的库带前缀libfoo.so 而是foo.so
set_target_properties(${PROJECT_NAME} PROPERTIES PREFIX "")


```

