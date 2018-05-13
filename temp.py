for count in range(0, 10):
    # check type of theater
    if result_tracking == 1:
        if type_script == 1:
            [new_url, likes] = self.__get_faster__data_image_theater__(obj)
        else:
            [new_url, likes] = ['', '']
        # check condition
        # if new_url[0] in array_checkin:
        #     break
        # array_checkin.extend(new_url)
    self.next_image_theater()
    print('next image')
    [result_tracking, obj] = self.tracking_theater()