# Add inputs and outputs from these tool invocations to the build variables
C_SRCS += \
../Utils/ip_parser.c \
../Utils/network.c

OBJS += \
./Utils/ip_parser.o \
./Utils/network.o

C_DEPS += \
./Utils/ip_parser.d \
./Utils/network.d


# Each subdirectory must supply rules for building sources it contributes
Utils/%.o: ../Utils/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C Compiler'
	gcc -D__GCC_POSIX__=1 -DDEBUG_BUILD=1 -DUSE_STDIO=1 -I.. -I../Utils -I../FreeRTOS_Kernel/include -I../FreeRTOS_Kernel/portable/GCC/Posix -O0 -g -Wall -c -fmessage-length=0 -pthread -lrt -Wno-pointer-sign -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o"$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

